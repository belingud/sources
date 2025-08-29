import json
import logging
import os
import secrets
from datetime import datetime

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# --------------- 日志配置 -------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("cohere-proxy")

# --------------- 应用初始化 -----------------
app = FastAPI(
    title="Cohere OpenAI代理",
    description="一个生产级别的、完全兼容的代理。",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- 常量配置 -------------------
COHERE_BASE_URL = os.getenv("COHERE_BASE_URL", "https://api.cohere.ai")
COHERE_USER_AGENT = "cohere-py/5.6.0"
BASE_CREATED = 1700000000

# 参数映射表
COHERE_TO_OPENAI_MAP = {
    "temperature": "temperature",
    "max_tokens": "max_tokens",
    "seed": "seed",
    "stop": "stop_sequences",
}


# --------------- 工具函数 -------------------
def get_httpx_client():
    return httpx.AsyncClient(timeout=httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=10.0))


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10),
    retry=(
        retry_if_exception_type(httpx.ConnectError)
        | retry_if_exception_type(httpx.ConnectTimeout)
        | retry_if_exception_type(httpx.ReadTimeout)
    ),
    reraise=True,
)
async def make_request_with_retry(client, method, url, **kwargs):
    logger.debug(f"[PROXY -> COHERE] Request: {method} {url}")
    if "json" in kwargs:
        logger.debug(
            f"[PROXY -> COHERE] Body:\n{json.dumps(kwargs.get('json'), ensure_ascii=False, indent=2)}"
        )
    response = await client.request(method, url, **kwargs)
    logger.info(f"Upstream Response | {method} | {url} | -> | {response.status_code}")
    return response


async def get_auth_key(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        key = auth_header[7:].strip()
        if key:
            return key

    key = request.query_params.get("key")
    if key:
        return key.strip()

    try:
        body = await request.json()
        if isinstance(body, dict) and "key" in body:
            return str(body["key"]).strip()
    except Exception:
        pass

    raise HTTPException(status_code=401, detail={"error": {"message": "未提供Cohere API密钥。"}})


def map_finish_reason(cohere_reason: str) -> str:
    mapping = {
        "COMPLETE": "stop",
        "MAX_TOKENS": "length",
        "TOO_MANY_TOKENS": "length",
        "ERROR": "error",
        "CONTENT_FILTERED": "content_filter",
        "TOOL_CALL": "tool_calls",
    }
    return mapping.get(cohere_reason.upper(), "stop")


# --------------- 路由定义 -------------------


@app.get("/", include_in_schema=False)
async def root():
    html = """
    <html><body style="text-align:center; font-family:sans-serif; margin-top:4rem;">
        <h1>✅ Cohere OpenAI代理运行就绪</h1>
    </body></html>
    """
    return Response(content=html, media_type="text/html")


@app.get("/v1/models")
async def list_models(request: Request):
    """
    获取所有可用的Cohere模型。
    """
    auth = await get_auth_key(request)
    headers = {"Authorization": f"Bearer {auth}", "User-Agent": COHERE_USER_AGENT}

    async with get_httpx_client() as client:
        res = await make_request_with_retry(
            client, "GET", f"{COHERE_BASE_URL}/v1/models", headers=headers
        )

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    raw_models = res.json().get("models", [])
    openai_models = []

    for idx, model in enumerate(raw_models):
        name = model.get("name")
        if not name:
            continue

        # ✅ 安全处理null字段
        features = model.get("features") or []
        endpoints = model.get("endpoints") or []

        capabilities = {
            "chat": "chat" in endpoints,
            "embed": "embed" in endpoints,
            "rerank": "rerank" in endpoints,
            "vision": model.get("supports_vision", False) or "vision" in features,
            "tools": "tools" in features or "strict_tools" in features,
            "reasoning": "reasoning" in features,
            "json_mode": "json_mode" in features,
        }

        openai_models.append(
            {
                "id": name,
                "object": "model",
                "created": BASE_CREATED + idx,
                "owned_by": "cohere",
                "capabilities": capabilities,
            }
        )

    return {"object": "list", "data": openai_models}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    处理聊天补全请求，代理到Cohere v2 API。
    """
    auth = await get_auth_key(request)

    try:
        body = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"无效的JSON格式: {e}") from None

    messages_for_cohere = [
        {"role": msg.get("role", "user").lower(), "content": msg.get("content", "")}
        for msg in body.get("messages", [])
    ]

    cohere_payload = {
        "model": body.get("model", "command-r"),
        "messages": messages_for_cohere,
        "stream": bool(body.get("stream", False)),
    }

    # 映射标准参数
    for openai_key, cohere_key in COHERE_TO_OPENAI_MAP.items():
        if openai_key in body:
            cohere_payload[cohere_key] = body[openai_key]

    if "top_p" in body:
        cohere_payload["p"] = min(float(body["top_p"]), 0.99)

    if "tools" in body:
        cohere_payload["tools"] = body["tools"]

    headers = {
        "Authorization": f"Bearer {auth}",
        "Content-Type": "application/json",
        "User-Agent": COHERE_USER_AGENT,
    }
    created = int(datetime.utcnow().timestamp())
    cohere_endpoint = f"{COHERE_BASE_URL}/v2/chat"

    # ========== 处理非流式请求 ==========
    if not cohere_payload["stream"]:
        async with get_httpx_client() as client:
            res = await make_request_with_retry(
                client, "POST", cohere_endpoint, json=cohere_payload, headers=headers
            )

        if res.status_code != 200:
            error_text = (await res.aread()).decode("utf-8", "replace")
            logger.error(f"上游错误 {res.status_code}: {error_text}")
            raise HTTPException(status_code=res.status_code, detail=error_text)

        raw_response = res.json()

        # ✅ 提取usage
        usage_info = raw_response.get("usage", {})
        billed_units = usage_info.get("billed_units", {})
        prompt_tokens = billed_units.get("input_tokens", 0)
        completion_tokens = billed_units.get("output_tokens", 0)
        total_tokens = prompt_tokens + completion_tokens

        # ✅ 智能解析message.content
        content_blocks = raw_response.get("message", {}).get("content", [])
        message_content = {"role": "assistant"}

        # 判断是否涉及工具调用
        tool_calls_requested = "tools" in body and body["tools"]
        has_tool_calls = any(item.get("type") == "tool-call" for item in content_blocks)

        if tool_calls_requested and has_tool_calls:
            # 构造 tool_calls 数组
            tool_calls = []
            for block in content_blocks:
                if block.get("type") == "tool-call":
                    tc = block.get("tool_call", {})
                    tool_calls.append(
                        {
                            "id": tc.get("id"),
                            "function": {
                                "name": tc.get("name"),
                                "arguments": tc.get("arguments", "{}"),  # 注意：这里应该是字符串
                            },
                            "type": "function",
                        }
                    )
            message_content["tool_calls"] = tool_calls  # type: ignore

        else:
            # 提取文本
            content_text = ""
            for block in content_blocks:
                if block.get("type") == "text":
                    content_text += block.get("text", "")
            message_content["content"] = content_text

        return {
            "id": raw_response.get("id", f"chatcmpl-{secrets.token_hex(12)}"),
            "object": "chat.completion",
            "created": created,
            "model": cohere_payload["model"],
            "choices": [
                {
                    "index": 0,
                    "message": message_content,
                    "finish_reason": map_finish_reason(raw_response.get("finish_reason", "STOP")),
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            },
        }

    else:

        async def generate():
            def create_chunk(delta=None, finish_reason=None, usage_data=None):
                chunk = {
                    "id": f"chatcmpl-{secrets.token_hex(12)}",
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": cohere_payload["model"],
                }
                if usage_data:
                    chunk["usage"] = usage_data
                else:
                    chunk["choices"] = [
                        {"index": 0, "delta": delta or {}, "finish_reason": finish_reason}
                    ]
                return chunk

            def format_chunk(c):
                return f"data: {json.dumps(c, ensure_ascii=False)}\n\n"

            yield format_chunk(create_chunk(delta={"role": "assistant"}))

            try:
                async with get_httpx_client() as client:
                    async with client.stream(
                        "POST", cohere_endpoint, json=cohere_payload, headers=headers
                    ) as stream:
                        if stream.status_code != 200:
                            err = (await stream.aread()).decode("utf-8", "replace")
                            logger.error(f"上游错误: {err}")
                            yield format_chunk(
                                create_chunk(
                                    delta={"content": f"[ERROR] {err}"}, finish_reason="error"
                                )
                            )
                            return

                        buffer = ""
                        async for raw in stream.aiter_bytes():
                            buffer += raw.decode("utf-8", "replace")
                            lines = buffer.split("\n")
                            buffer = lines.pop()

                            for line in lines:
                                if not line.startswith("data:"):
                                    continue
                                data = line[5:].strip()
                                if not data:
                                    continue
                                if data == "[DONE]":
                                    yield "data: [DONE]\n\n"
                                    return

                                try:
                                    event = json.loads(data)
                                    event_type = event.get("type")

                                    if event_type == "content-delta":
                                        text = (
                                            event.get("delta", {})
                                            .get("message", {})
                                            .get("content", {})
                                            .get("text", "")
                                        )
                                        if text:
                                            yield format_chunk(
                                                create_chunk(delta={"content": text})
                                            )

                                    elif event_type == "message-end":
                                        delta = event.get("delta", {})
                                        finish_reason = map_finish_reason(
                                            delta.get("finish_reason", "COMPLETE")
                                        )

                                        # 流式 usage
                                        usage_requested = body.get("stream_options", {}).get(
                                            "include_usage"
                                        )
                                        if usage_requested:
                                            u_info = delta.get("usage", {})
                                            b_units = u_info.get("billed_units", {})
                                            yield format_chunk(
                                                create_chunk(
                                                    usage_data={
                                                        "prompt_tokens": b_units.get(
                                                            "input_tokens", 0
                                                        ),
                                                        "completion_tokens": b_units.get(
                                                            "output_tokens", 0
                                                        ),
                                                        "total_tokens": b_units.get(
                                                            "input_tokens", 0
                                                        )
                                                        + b_units.get("output_tokens", 0),
                                                    }
                                                )
                                            )

                                        yield format_chunk(
                                            create_chunk(finish_reason=finish_reason)
                                        )
                                        yield "data: [DONE]\n\n"
                                        return

                                except Exception as e:
                                    logger.error(f"解析流式事件失败: {e}")
                                    yield format_chunk(
                                        create_chunk(
                                            delta={"content": "[解析错误]"}, finish_reason="error"
                                        )
                                    )
                                    return

            except Exception as e:
                logger.error(f"流式连接失败: {e}")
                yield format_chunk(
                    create_chunk(delta={"content": "[连接失败]"}, finish_reason="error")
                )
            finally:
                yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/v1/embeddings")
async def create_embeddings(request: Request):
    auth = await get_auth_key(request)
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="无效的JSON") from None

    input_texts = body.get("input")
    if isinstance(input_texts, str):
        input_texts = [input_texts]
    elif not input_texts:
        input_texts = [""]

    model = body.get("model", "embed-english-v3.0")
    headers = {
        "Authorization": f"Bearer {auth}",
        "Content-Type": "application/json",
        "User-Agent": COHERE_USER_AGENT,
    }

    async with get_httpx_client() as client:
        res = await make_request_with_retry(
            client,
            "POST",
            f"{COHERE_BASE_URL}/v1/embed",
            json={"texts": input_texts, "model": model, "input_type": "search_document"},
            headers=headers,
        )

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    data = res.json()

    return {
        "object": "list",
        "model": model,
        "data": [
            {"object": "embedding", "embedding": vec, "index": idx}
            for idx, vec in enumerate(data.get("embeddings", []))
        ],
        "usage": {"prompt_tokens": 0, "total_tokens": 0},
    }

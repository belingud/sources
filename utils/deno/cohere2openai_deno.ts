// Cohere to OpenAI API Proxy for Deno Deploy
// 基于 cohere2openai_deno.py 的 TypeScript 实现

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";

// --------------- 常量配置 -------------------
const COHERE_BASE_URL = Deno.env.get("COHERE_BASE_URL") || "https://api.cohere.ai";
const COHERE_USER_AGENT = "cohere-py/5.6.0";
const BASE_CREATED = 1700000000;
const LOG_LEVEL = Deno.env.get("LOG_LEVEL") || "INFO";

// 参数映射表
const COHERE_TO_OPENAI_MAP: Record<string, string> = {
    temperature: "temperature",
    max_tokens: "max_tokens",
    seed: "seed",
    stop: "stop_sequences",
};

// --------------- 工具函数 -------------------
function log(level: string, message: string, ...args: any[]) {
    const timestamp = new Date().toISOString();
    const logLevels = ["DEBUG", "INFO", "WARN", "ERROR"];
    const currentLevelIndex = logLevels.indexOf(LOG_LEVEL.toUpperCase());
    const messageLevelIndex = logLevels.indexOf(level.toUpperCase());

    if (messageLevelIndex >= currentLevelIndex) {
        console.log(`${timestamp} | ${level.padEnd(8)} | ${message}`, ...args);
    }
}

async function makeRequestWithRetry(
    url: string,
    options: RequestInit = {},
    maxRetries = 3
): Promise<Response> {
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            log(
                "DEBUG",
                `[PROXY -> COHERE] Request: ${options.method || "GET"} ${url}`
            );

            const response = await fetch(url, {
                ...options,
                signal: AbortSignal.timeout(300000), // 5 minutes timeout
            });

            log(
                "INFO",
                `Upstream Response | ${options.method || "GET"} | ${url} | -> | ${response.status
                }`
            );
            return response;
        } catch (error) {
            lastError = error as Error;
            log("WARN", `Attempt ${attempt} failed: ${lastError.message}`);

            if (attempt < maxRetries) {
                const delay = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
                await new Promise((resolve) => setTimeout(resolve, delay));
            }
        }
    }

    throw lastError;
}

function getAuthKey(request: Request): string {
    // 从 Authorization header 获取
    const authHeader = request.headers.get("Authorization");
    if (authHeader && authHeader.startsWith("Bearer ")) {
        const key = authHeader.slice(7).trim();
        if (key) return key;
    }

    // 从 URL 参数获取
    const url = new URL(request.url);
    const keyParam = url.searchParams.get("key");
    if (keyParam) return keyParam.trim();

    throw new Response(
        JSON.stringify({ error: { message: "未提供Cohere API密钥。" } }),
        { status: 401, headers: { "Content-Type": "application/json" } }
    );
}

function mapFinishReason(cohereReason: string): string {
    const mapping: Record<string, string> = {
        COMPLETE: "stop",
        MAX_TOKENS: "length",
        TOO_MANY_TOKENS: "length",
        ERROR: "error",
        CONTENT_FILTERED: "content_filter",
        TOOL_CALL: "tool_calls",
    };
    return mapping[cohereReason.toUpperCase()] || "stop";
}

function generateId(prefix = "chatcmpl"): string {
    const bytes = new Uint8Array(12);
    crypto.getRandomValues(bytes);
    const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join(
        ""
    );
    return `${prefix}-${hex}`;
}

// --------------- 路由处理器 -------------------
async function handleRoot(): Promise<Response> {
    const html = `
    <html><body style="text-align:center; font-family:sans-serif; margin-top:4rem;">
        <h1>✅ Cohere OpenAI代理运行就绪</h1>
    </body></html>
  `;
    return new Response(html, {
        headers: { "Content-Type": "text/html" },
    });
}

async function handleModels(request: Request): Promise<Response> {
    try {
        const auth = getAuthKey(request);
        const headers = {
            Authorization: `Bearer ${auth}`,
            "User-Agent": COHERE_USER_AGENT,
        };

        const response = await makeRequestWithRetry(
            `${COHERE_BASE_URL}/v1/models`,
            { headers }
        );

        if (!response.ok) {
            return new Response(await response.text(), { status: response.status });
        }

        const data = await response.json();
        const rawModels = data.models || [];
        const openaiModels: any[] = [];

        for (let idx = 0; idx < rawModels.length; idx++) {
            const model = rawModels[idx];
            const name = model.name;
            if (!name) continue;

            // 安全处理null字段
            const features = model.features || [];
            const endpoints = model.endpoints || [];

            const capabilities = {
                chat: endpoints.includes("chat"),
                embed: endpoints.includes("embed"),
                rerank: endpoints.includes("rerank"),
                vision: model.supports_vision || features.includes("vision"),
                tools: features.includes("tools") || features.includes("strict_tools"),
                reasoning: features.includes("reasoning"),
                json_mode: features.includes("json_mode"),
            };

            openaiModels.push({
                id: name,
                object: "model",
                created: BASE_CREATED + idx,
                owned_by: "cohere",
                capabilities,
            });
        }

        return new Response(
            JSON.stringify({ object: "list", data: openaiModels }),
            { headers: { "Content-Type": "application/json" } }
        );
    } catch (error) {
        if (error instanceof Response) {
            return error;
        }
        log("ERROR", "Models endpoint error:", error);
        return new Response(
            JSON.stringify({ error: { message: "Internal server error" } }),
            { status: 500, headers: { "Content-Type": "application/json" } }
        );
    }
}

async function handleChatCompletions(request: Request): Promise<Response> {
    try {
        const auth = getAuthKey(request);
        const body = await request.json();

        const messagesForCohere = (body.messages || []).map((msg: any) => ({
            role: (msg.role || "user").toLowerCase(),
            content: msg.content || "",
        }));

        const coherePayload: any = {
            model: body.model || "command-r",
            messages: messagesForCohere,
            stream: Boolean(body.stream),
        };

        // 映射标准参数
        for (const [openaiKey, cohereKey] of Object.entries(COHERE_TO_OPENAI_MAP)) {
            if (openaiKey in body) {
                coherePayload[cohereKey] = body[openaiKey];
            }
        }

        if ("top_p" in body) {
            coherePayload.p = Math.min(parseFloat(body.top_p), 0.99);
        }

        if ("tools" in body) {
            coherePayload.tools = body.tools;
        }

        const headers = {
            Authorization: `Bearer ${auth}`,
            "Content-Type": "application/json",
            "User-Agent": COHERE_USER_AGENT,
        };

        const created = Math.floor(Date.now() / 1000);
        const cohereEndpoint = `${COHERE_BASE_URL}/v2/chat`;

        // ========== 处理非流式请求 ==========
        if (!coherePayload.stream) {
            const response = await makeRequestWithRetry(cohereEndpoint, {
                method: "POST",
                headers,
                body: JSON.stringify(coherePayload),
            });

            if (!response.ok) {
                const errorText = await response.text();
                log("ERROR", `上游错误 ${response.status}: ${errorText}`);
                return new Response(errorText, { status: response.status });
            }

            const rawResponse = await response.json();

            // 提取usage
            const usageInfo = rawResponse.usage || {};
            const billedUnits = usageInfo.billed_units || {};
            const promptTokens = billedUnits.input_tokens || 0;
            const completionTokens = billedUnits.output_tokens || 0;
            const totalTokens = promptTokens + completionTokens;

            // 智能解析message.content
            const contentBlocks = rawResponse.message?.content || [];
            const messageContent: any = { role: "assistant" };

            // 判断是否涉及工具调用
            const toolCallsRequested = "tools" in body && body.tools;
            const hasToolCalls = contentBlocks.some(
                (item: any) => item.type === "tool-call"
            );

            if (toolCallsRequested && hasToolCalls) {
                // 构造 tool_calls 数组
                const toolCalls: any[] = [];
                for (const block of contentBlocks) {
                    if (block.type === "tool-call") {
                        const tc = block.tool_call || {};
                        toolCalls.push({
                            id: tc.id,
                            function: {
                                name: tc.name,
                                arguments: tc.arguments || "{}",
                            },
                            type: "function",
                        });
                    }
                }
                messageContent.tool_calls = toolCalls;
            } else {
                // 提取文本
                let contentText = "";
                for (const block of contentBlocks) {
                    if (block.type === "text") {
                        contentText += block.text || "";
                    }
                }
                messageContent.content = contentText;
            }

            return new Response(
                JSON.stringify({
                    id: rawResponse.id || generateId(),
                    object: "chat.completion",
                    created,
                    model: coherePayload.model,
                    choices: [
                        {
                            index: 0,
                            message: messageContent,
                            finish_reason: mapFinishReason(
                                rawResponse.finish_reason || "STOP"
                            ),
                        },
                    ],
                    usage: {
                        prompt_tokens: promptTokens,
                        completion_tokens: completionTokens,
                        total_tokens: totalTokens,
                    },
                }),
                { headers: { "Content-Type": "application/json" } }
            );
        }

        // ========== 处理流式请求 ==========
        const stream = new ReadableStream({
            async start(controller) {
                function createChunk(
                    delta?: any,
                    finishReason?: string,
                    usageData?: any
                ) {
                    const chunk: any = {
                        id: generateId(),
                        object: "chat.completion.chunk",
                        created,
                        model: coherePayload.model,
                    };

                    if (usageData) {
                        chunk.usage = usageData;
                    } else {
                        chunk.choices = [
                            {
                                index: 0,
                                delta: delta || {},
                                finish_reason: finishReason || null,
                            },
                        ];
                    }
                    return chunk;
                }

                function formatChunk(c: any): Uint8Array {
                    const data = `data: ${JSON.stringify(c)}\n\n`;
                    return new TextEncoder().encode(data);
                }

                // 发送初始角色信息
                controller.enqueue(formatChunk(createChunk({ role: "assistant" })));

                try {
                    const response = await makeRequestWithRetry(cohereEndpoint, {
                        method: "POST",
                        headers,
                        body: JSON.stringify(coherePayload),
                    });

                    if (!response.ok) {
                        const err = await response.text();
                        log("ERROR", `上游错误: ${err}`);
                        controller.enqueue(
                            formatChunk(createChunk({ content: `[ERROR] ${err}` }, "error"))
                        );
                        controller.close();
                        return;
                    }

                    if (!response.body) {
                        throw new Error("No response body");
                    }

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    let buffer = "";

                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;

                        buffer += decoder.decode(value, { stream: true });
                        const lines = buffer.split("\n");
                        buffer = lines.pop() || "";

                        for (const line of lines) {
                            if (!line.startsWith("data:")) continue;

                            const data = line.slice(5).trim();
                            if (!data) continue;

                            if (data === "[DONE]") {
                                controller.enqueue(
                                    new TextEncoder().encode("data: [DONE]\n\n")
                                );
                                controller.close();
                                return;
                            }

                            try {
                                const event = JSON.parse(data);
                                const eventType = event.type;

                                if (eventType === "content-delta") {
                                    const text = event.delta?.message?.content?.text || "";
                                    if (text) {
                                        controller.enqueue(
                                            formatChunk(createChunk({ content: text }))
                                        );
                                    }
                                } else if (eventType === "message-end") {
                                    const delta = event.delta || {};
                                    const finishReason = mapFinishReason(
                                        delta.finish_reason || "COMPLETE"
                                    );

                                    // 流式 usage
                                    const usageRequested = body.stream_options?.include_usage;
                                    if (usageRequested) {
                                        const uInfo = delta.usage || {};
                                        const bUnits = uInfo.billed_units || {};
                                        controller.enqueue(
                                            formatChunk(
                                                createChunk(undefined, undefined, {
                                                    prompt_tokens: bUnits.input_tokens || 0,
                                                    completion_tokens: bUnits.output_tokens || 0,
                                                    total_tokens:
                                                        (bUnits.input_tokens || 0) +
                                                        (bUnits.output_tokens || 0),
                                                })
                                            )
                                        );
                                    }

                                    controller.enqueue(
                                        formatChunk(createChunk(undefined, finishReason))
                                    );
                                    controller.enqueue(
                                        new TextEncoder().encode("data: [DONE]\n\n")
                                    );
                                    controller.close();
                                    return;
                                }
                            } catch (error) {
                                log("ERROR", "解析流式事件失败:", error);
                                controller.enqueue(
                                    formatChunk(createChunk({ content: "[解析错误]" }, "error"))
                                );
                                controller.close();
                                return;
                            }
                        }
                    }
                } catch (error) {
                    log("ERROR", "流式连接失败:", error);
                    controller.enqueue(
                        formatChunk(createChunk({ content: "[连接失败]" }, "error"))
                    );
                } finally {
                    controller.enqueue(new TextEncoder().encode("data: [DONE]\n\n"));
                    controller.close();
                }
            },
        });

        return new Response(stream, {
            headers: {
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                Connection: "keep-alive",
            },
        });
    } catch (error) {
        if (error instanceof Response) {
            return error;
        }
        log("ERROR", "Chat completions error:", error);
        return new Response(
            JSON.stringify({ error: { message: "Internal server error" } }),
            { status: 500, headers: { "Content-Type": "application/json" } }
        );
    }
}

async function handleEmbeddings(request: Request): Promise<Response> {
    try {
        const auth = getAuthKey(request);
        const body = await request.json();

        let inputTexts = body.input;
        if (typeof inputTexts === "string") {
            inputTexts = [inputTexts];
        } else if (!inputTexts) {
            inputTexts = [""];
        }

        const model = body.model || "embed-english-v3.0";
        const headers = {
            Authorization: `Bearer ${auth}`,
            "Content-Type": "application/json",
            "User-Agent": COHERE_USER_AGENT,
        };

        const response = await makeRequestWithRetry(`${COHERE_BASE_URL}/v1/embed`, {
            method: "POST",
            headers,
            body: JSON.stringify({
                texts: inputTexts,
                model,
                input_type: "search_document",
            }),
        });

        if (!response.ok) {
            return new Response(await response.text(), { status: response.status });
        }

        const data = await response.json();

        return new Response(
            JSON.stringify({
                object: "list",
                model,
                data: (data.embeddings || []).map((vec: number[], idx: number) => ({
                    object: "embedding",
                    embedding: vec,
                    index: idx,
                })),
                usage: { prompt_tokens: 0, total_tokens: 0 },
            }),
            { headers: { "Content-Type": "application/json" } }
        );
    } catch (error) {
        if (error instanceof Response) {
            return error;
        }
        log("ERROR", "Embeddings error:", error);
        return new Response(
            JSON.stringify({ error: { message: "Internal server error" } }),
            { status: 500, headers: { "Content-Type": "application/json" } }
        );
    }
}

// --------------- 主路由处理器 -------------------
async function handler(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const { pathname, method } = {
        pathname: url.pathname,
        method: request.method,
    };

    // 添加CORS头
    const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    };

    // 处理 OPTIONS 请求
    if (method === "OPTIONS") {
        return new Response(null, { status: 200, headers: corsHeaders });
    }

    let response: Response;

    try {
        if (pathname === "/" && method === "GET") {
            response = await handleRoot();
        } else if (pathname === "/v1/models" && method === "GET") {
            response = await handleModels(request);
        } else if (pathname === "/v1/chat/completions" && method === "POST") {
            response = await handleChatCompletions(request);
        } else if (pathname === "/v1/embeddings" && method === "POST") {
            response = await handleEmbeddings(request);
        } else {
            response = new Response("Not Found", { status: 404 });
        }
    } catch (error) {
        log("ERROR", "Handler error:", error);
        response = new Response(
            JSON.stringify({ error: { message: "Internal server error" } }),
            { status: 500, headers: { "Content-Type": "application/json" } }
        );
    }

    // 为所有响应添加CORS头
    Object.entries(corsHeaders).forEach(([key, value]) => {
        response.headers.set(key, value);
    });

    return response;
}

// --------------- 启动服务器 -------------------
Deno.serve(handler);
console.log("🚀 Cohere OpenAI代理服务器启动在端口 8000");




uvicorn使用spawn方式部署多个worker，代码在：uvicorn.subprocess文件中，uvicorn团队已经不记得为什么使用spawn

```python
spawn = multiprocessing.get_context("spawn")
```

多个worker会导致重复配置，比如重复配置middleware：

```python
app.user_middleware
# [Middleware(GlobalErrorMiddleware), Middleware(GlobalRequestMiddleware), Middleware(GlobalErrorMiddleware), Middleware(GlobalRequestMiddleware)]
```
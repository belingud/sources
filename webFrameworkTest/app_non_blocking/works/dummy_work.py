import asyncio
import time
import typing
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from flask import Flask, current_app, request, g
from loguru import logger


def callback(future: asyncio.Future, *args, **kwargs):
    """
    async function callback
    """
    logger.info(f"passed future object is {future}")
    del future


def delay(func: typing.Callable, app: Flask, *args, **kwargs):
    """
    Publish a future async work
    """
    assert callable(func), "``func`` param has to be a callable function"
    # global future
    executor = ThreadPoolExecutor(1)
    q = Queue(1)
    # future = current_app.event_loop.run_in_executor(None, func, *[1, 2, 3], **kwargs)
    future = current_app.event_loop.run_in_executor(executor, func, *[kwargs["num"], q])
    executor.submit(func, *[q])
    q.put(future)


def fake_work(*args, **kwargs):
    """
    Simulate a long time cost work
    """
    logger.info("in longcost work function")
    logger.info(f"args: {args}")
    time.sleep(10)
    try:
        with current_app.app_context():
            logger.info(f"Request obj after a request life circle: {request}")
            logger.info(f"G obj after a request life circle: {g}")
    except RuntimeError:
        pass
    logger.info("finished longcost work")
    logger.info(f"args: {args}")
    q = args[-1]
    future = q.get()
    callback(future)

Flask是一个同步的，使用WSGI协议的Python WEB框架，他不能和sanic，fastapi那样使用异步的事件循环来处理请求，也不能利用uvicorn等的ASGI服务器来加速自己，耗时任务需要发布到Celery来执行。

因为在Flask中遇到了耗时的任务和代码，需要阻塞等待，绝大部分任务都分发到了Celery中，统一处理。所以有了在同步服务器中使用异步代码来处理任务，来看对现有程序的影响。

这里提供一种思路，在flask项目中，使用asyncio模块，来实现异步任务。主要是利用了asyncio的future对象，发布异步执行的命令之后，方法会在异步的executor中执行，不阻塞当前的代码出行。

**先说结论**

1. 使用线程池或者进程池executor或者直接发布，python会在非阻塞的环境中执行这段代码
2. 因为loop没有对发布的event进行管理(我是这么理解的)，不监控事件的执行状态，不能实现callback回调
3. 使用了线程共享某些对象的方法，例如future对象，实现了任务执行完毕，执行指定代码

在这里记录一下我的思路，详细的代码会在末尾给出。

首先是创建一个flask的app对象，给这个对象一个事件循环，让他用这个时间循环来发布异步的任务。

```python
#! /usr/bin/env python
# A test for asyncio usage in flask app
import asyncio

from flask import Flask, current_app, jsonify, request
from loguru import logger

from works.dummy_work import delay, fake_work

app = Flask(__name__)

if __name__ == "__main__":
    app.event_loop = asyncio.get_event_loop()
    try:
        app.run(debug=True)
    except Exception as e:
        logger.error(f'Error happened: {e}')
    finally:
        app.event_loop.stop()
        app.event_loop.run_until_complete(app.event_loop.shutdown_asyncgens())
        app.event_loop.close()
```

模拟一个耗时的任务

```python
def fake_work(*args, **kwargs):
    """
    Simulate a long time cost work
    """
    logger.info('In fake_work function')
    logger.info(f'Args: {args}')
    time.sleep(10)
    logger.info(f'Finished fake work')
```

一个发布异步任务的方法

```python
def delay(func: typing.Callable, app: Flask, *args, **kwargs):
    """
    Publish a future async work
    """
    assert callable(func), "``func`` param has to be a callable function"
    future = current_app.event_loop.run_in_executor(
        None, func, *args
        )
    future.add_done_callback(callback)
    logger.info('Add callback function to future obj')
```

一个回调函数，来测试执行成功后，能否实现回调

```python
def callback(future: asyncio.Future, *args, **kwargs):
    """
    async function callback
    """
    logger.info(f'Passed future object is {future}')
```

然后在接口中调用发布任务的逻辑

```python
@app.route('/test', methods=['GET'])
def index():
    delay(fake_work, current_app, num=request.args.get('num'))
    return jsonify({"msg": "ok"})
```

启动服务

```shell
> flask run
```

用httpie进行测试

```shell
> http :5000/test
HTTP/1.0 200 OK
Content-Length: 13
Content-Type: application/json
Date: Thu, 18 Jun 2020 07:38:05 GMT
Server: Werkzeug/1.0.1 Python/3.7.5

{
    "msg": "ok"
}
```

fake_work在sleep了10秒之后，打印了`Finish fake work`，但是没有回调。

可以看到实现了异步任务的发布和执行，为什么使用`run_in_executor`呢，因为一个异步的函数，在变成`coroutine`之后，内部的逻辑是不会执行的，只有在event loop接管这个coroutine之后，内部的逻辑才会执行，而同步的代码，比如上面的fake_work，让其被其它executor执行之后，内部的逻辑会继续执行，实际上，他还是一个同步的代码，会直接执行，但是，event loop将其交给了executor来执行，这里这个参数是None，实际上会调用默认的执行器，`concurrent.futures.ThreadPoolExecutor`对象，然后交给他来处理。

因为这是由event loop来发布的，所以你也可以等待他执行完，`loop.run_until_complete(future)`，使用这个方法还可以实现回调，但是会阻塞等待任务的执行，那就和我们的初衷不一样了。

其实看到时间循环的默认executor对象，我们就可以摆脱asyncio，直接使用executor来执行这个任务。

将发布异步任务的方法改为

```python
def delay(func: typing.Callable, app: Flask = None, *args, **kwargs):
    """
    Publish a future async work
    """
    assert callable(func), "``func`` param has to be a callable function"
    executor = ThreadPoolExecutor(1)
    # 也可以是一个进程池
    # executor = ProcessPoolExecutor()
    executor.submit(func, *args)
```

*实验结果在线程执行完成后，会自动退出，回收*

因为事件循环不能监控任务的进度状态，所以不能实现回调。

在任务最后调用其他逻辑，这里有一个问题，如果你需要把其他参数，或者一个在任务更高层的代码的数据，可以在线程间共享数据，使用全局变量，或者使用一个队列来通信。这里用队列来做

```python
def delay(func: typing.Callable, app: Flask, *args, **kwargs):
    """
    Publish a future async work
    """
    assert callable(func), "``func`` param has to be a callable function"
    # 默认会创建一个未传入参数的ThreadPoolExecutor，这里指定一个线程数
    executor = ThreadPoolExecutor(1)
    q = Queue(1)
    # 使用全局变量也可以在线程间共享
    # global future
    future = current_app.event_loop.run_in_executor(
        executor, func, *[q]
        )
    # executor.submit(func, *[q])
    q.put(future)
```

在发布的线程任务中获取这个变量

```python
def fake_work(*args, **kwargs):
    """
    Simulate a long time cost work
    """
    logger.info('in longcost work function')
    logger.info(f'args: {args}')
    time.sleep(10)
    q = args[-1]
    # 如果future是一个全局变量，可以在这里直接使用，而不用在队列里面获取
    future = q.get()
    callback(future)
    # del future
```

需要注意的一点是，无论任何方式，发布的非阻塞程序，都是在flask的请求生命周期之外的，首先不能使用flask的全局对象request，g和session，也不能使用`app.app_context()`来创建上下文环境，都会抛出`RuntimeError`异常。在非阻塞的程序中出现异常，需要单独捕获，可能不会在日志或控制台输出相应的错误提示，在debug时可以看到错误。

因为是创建线程去做了相应的工作，我使用了gunicorn来启动flask，模拟并发请求，并监控线程数，没有发现明显的隐患。后续会继续进行测试。
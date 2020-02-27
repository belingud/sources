
# celery

celery的使用以及在Django中的配置，不详细介绍，主要记录在Django中使用的坑点。

# 坑点

## 时区问题

celery默认的时区是世界标准时间，比东八区慢了8个小时，如果发布定时任务，一定要注意定时的时间，否则可能用了正确的方法，但是并没有调用成功

设置celery的时区可以在Django项目的`settings.py`中添加一条设置

```python
CELERY_TIMEZONE = 'Asia/Shanghai'
```

`django-celery`可以识别在设置中的时区

也可以在发布定时任务的时候，指定到当前的时区，使用Django自带的`get_current_timezone()`

```python
# 将需要设定的时间转换成当前时区的时间
from django.utils.timezone import get_current_timezone
import datetime

send_time = datetime.datetime.now() + datetime.timedelta(days=1)
tz = get_current_timezone()
send_time = tz.localize(send_time)
```

在使用异步任务的时候将转换后的时间传入到参数里面

```python
celery_task.apply_async(args=[], kwdg={}, eta=send_time)
```

当然，你也可以使用间隔时间执行异步任务，对应`apply_async()`里面的countdown参数

```python
celery_task.apply_async(countdown=seconds)
```

## celery的序列化问题

celery提供了两个序列化的格式，`pickle`和`json`，pickle是python一个序列化的库，可以实现多种格式数据的序列和反序列化，对应pickle和unpickle

设置中可以指定celery接受的数据格式，以及任务和结果的序列化器

```python
# settings.py
# celery允许接收的数据格式，可以是一个字符串，比如'json'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
# 异步任务的序列化器，也可以是json
CELERY_TASK_SERIALIZER = 'pickle'
# 任务结果的数据格式，也可以是json
CELERY_RESULT_SERIALIZER = 'pickle'
```

在Django中的使用尤其需要注意，如果你需要向异步任务传入一个queryset，需要将接收的格式和序列化器设置为'pickle'，即如上设置

> 不建议将ORM对象传给celery的异步任务，拿到的可能是过期数据，建议传递id

## 结果

如果不需要讲异步任务执行的结果进行处理，即异步任务的执行结果和业务逻辑关系不大，建议不存储celery异步任务的结果。

如果保留结果，celery将会为任务结果建立一个队列，并且一直等到异步任务给出结果才会将任务从队列中删除，创建和管理任务的开销很大，可以在这篇博客中看到：https://www.cnblogs.com/blaketairan/p/7136897.html

在Django的settings中设置忽略celery任务执行结果

```python
CELERY_IGNORE_RESULT = True
```

## 使用不同的queue

如果任务A比任务B更重要，而任务B的量非常大，重要的任务A就需要不断等待任务B完成后才能继续进行，这时候，可以使用不同的queue来保存任务，让不同的worker来执行两种任务

```python
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
    Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
）
```

然后自定义router来执行不同的任务

```python

CELERY_ROUTES = {
    'my_taskA': {'queue': 'for_task_A', 'routing_key': 'for_task_A'},
    'my_taskB': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
}
```

然后在启动celery时，指定不同的worker

```shell
celery worker -E -l INFO -n workerA -Q for_task_A celery worker -E -l INFO -n workerB -Q for_task_B
```

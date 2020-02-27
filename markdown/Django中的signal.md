# Django中的信号

一篇讲signal讲的比较好的文章：https://www.atemon.com/blog/django-signals/

Django中提供了一个“信号分发器”，允许被接耦合的应用在其他地方发生操作时会被通知到，在一个事件影响多处代码的情况下很有用。


你可以将多个方法绑定到发送的信号上，使Django在一次数据变动时，处理更多的业务逻辑。信号系统允许一个或多个发送者，将信号发送给一组接收者。

信号系统包含三个部分：

1. 发送者
2. 信号
3. 接收者

Django中内置了几个信号接收器，可以直接注册然后添加相应的操作

```python
pre_init  # 实例化一个数据库模型前
post_init  # 实例化一个数据库模型后

pre_save  # 保存数据前
post_save  # 保存数据后

pre_delete  # 删除数据前
post_delete  # 删除数据后

m2m_changed  # 多对多关系改变后

pre_migrate  # 迁移前
post_migrate  # 迁移后
# 更多的方法在后面详细讲解
```

##　接收器的简单使用

首先应该初始化你的APP配置，在APP的`apps.py`中，配置你的APP

```python
from django.apps import AppConfig


class TestAppConfig(AppConfig):
    name = 'test_app'

    def ready(self):
        # 启动应用后导入自定义的signal回调方法
        import test_app.signals
```

然后在`__init__.py`中注册你的配置

```python
# 绑定app config
default_app_config = 'test_app.apps.TestAppConfig'
```


如果使接收器生效需要将自定义的方法，连接到接收器上。有两种方式，使用`connect()`方法，或者使用装饰器`receiver()`

### 使用connect方法

语法为：

```python
Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)
```

参数：

- receiver ：当前信号连接的回调函数，也就是处理信号的函数。 
- sender ：指定从哪个发送方接收信号。 
- weak ： 是否弱引用
- dispatch_uid ：信号接收器的唯一标识符，以防信号多次发送。


关于weak参数的理解，可以参考：

> weak – Django stores signal handlers as weak references by     default. 
> Thus, if your receiver is a local function, it may be garbage collected. 
> To prevent this, pass weak=False when you call the signal’s connect() method.


```python
from djangp.db.models.signals import post_save
from app.models import AppModel


def save_callback(sender, instance, **kwargs):
    """
    对象保存后的回调方法
    """
    print(sender)
    print(instance)
    print(kwargs)
    print('ORM has saved the object and now in callback method')


# sender是一个model，当model对象保存到数据库中时，自动调用这个回调函数
post_save.connect(save_callback, sender=AppModel)
```

### 使用register装饰器

`receiver()`装饰器接受的参数和`connect()`方法相同

使用receiver来注册信号接受函数：

```python
from django.core.signals import request_finished
from django.dispatch import receiver


@receiver(request_finished)
def finished_callback(sender, **kwargs):
    print(sender)
    print(kwargs)
    print('request finished and now in callback method')
```

具体使用哪种方式看个人习惯。

### 防止信号重复

为了防止信号重复，可以设置`dispatch_uid`参数来标识你的接收器，标识符通常是一个字符串，如下所示：

```python
from django.core.signals import request_finished

request_finished.connect(finished_callback, dispatch_uid='first_callback_id')
```

### 发送信号

在试图或其他的业务逻辑里面，向信号接收器发送信号：

```python
save_callback.sende(sender='some function or class', args1='args1', arg2='arg2')
```

在选择发送信号的方式有两种一种使用Signal.send，还有一种是Signal.send_robut。

`send()`与`send_robust()`处理接收器功能引起的异常的方式不同。

`send()`并不能捕获由接收器提出的任何异常; 它只是允许错误传播。因此，在面对错误时，不是所有接收器都可以被通知信号。

`send_robust()`捕获从Python Exception类派生的所有错误，并确保所有接收器都收到信号通知。如果发生错误，则会在引发错误的接收器的元组对中返回错误实例。

### 断开信号

也可以将接收器的信号断开：

```python
from django.dispatch import Signal
Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)
```

## Django内置的信号接收器

Django内置多个信号接收器，可以直接将自己的业务逻辑直接注册到信号接受器上，接受的参数如下：

**关于modles的信号接收器**

```python
from django.db.models import signals

signals.pre_init(sender, *args, **kwargs)
signals.post_init(sender, instance)
signals.pre_save(sender, instance, raw, using, update_fields)
signals.post_save(sender, instance, raw, using, update_fields)
signals.pre_delete(sender, instance, using)
signals.post_delete(sender, instance, using)
```
m2m_changed比较特殊，是ManyToManyField发送的，实现了`pre_save`/`post_save`和`pre_delete`/`post_delete`


参数：

- sender：描述ManyToManyField的中间模型类，这个中间模型类会在一个many-to-many字段被定义时自动被创建。我们可以通过使用many-to-many字段的through属性来访问它

- instance：被更新的多对多关系的实例。它可以是上面的sender，也可以是ManyToManyField的关系类。

- action：指明作用于关系更新类型的字符串，它可以是以下几种情况：

  - "pre_add"/"post_add"：在向关系发送一个或多个对象前 / 后发送

  - "pre_remove/post_remove"：从关系中删除一个或多个对象前 / 后发送

  - "pre_clear/post_clear"：在关系解除之前 / 之后发送

- reverse：正在修改的是正向关系或者反向关系，正向False，反向为True

- model：被添加、删除或清除的对象的类

- pk_set：对于add/remove等，pk_set是一个从关系中添加或删除的对象的主键 的集合， 对于clear，pk_set为None


**关于请求的信号接收器**

```python
from django.core import signals

signals.request_started(sender, *args, **kwargs)
signals.request_finished(sender, *args, **kwargs)
signals.got_request_exception(sender, *args, **kwargs)
```



# 一些可以更好使用python命令行、编码的 **pypi** 库

## pdir2：

python的美化`dir()`方法的输出结果

```shell
pip install pdir
```

github地址：https://github.com/laike9m/pdir2

使用：

```python
import pdir
import requests

resp = requests.get('www.baidu.com')

pdir(resp)
```

## better-exception:

美化python错误提示，每个变量、语法等的错误，都会有明显的标示

```shell
pip install better-exception
```

Pretty and more helpful exceptions in Python, automatically.

github地址：https://github.com/Qix-/better-exceptions

使用：

```shell
pip install better-exception

# 环境变量
export BETTER_EXCEPTIONS=1  # Linux / OSX
setx BETTER_EXCEPTIONS 1    # Windows
```

可以在命令行和python文件中使用。

命令行：

```shell
$ python -m better_exceptions
Type "help", "copyright", "credits" or "license" for more information.
(BetterExceptionsConsole)
>>>
```

*在ipython中使用没有语法高亮，不建议，等作者优化好*

python文件中使用：

```python
import better_exceptions
better_exceptions.MAX_LENGTH = None
```

在django中使用better-exception，需要加入一个中间件：

```python
# middlewares.py
import sys
from better_exceptions import excepthook


class BetterExceptionsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        excepthook(exception.__class__, exception, sys.exc_info()[2])
        return None
```

```python
# settings.py
MIDDLEWARE = [
...
    'myapp.middleware.BetterExceptionsMiddleware',
]
```

## fake

fake是一个用于生成假数据的库，支持多种语言，你值得拥有。示例代码：

```python
fake.address()
# '辽宁省雪市静安廉街b座 998259'

fake.street_address()
# '巢湖街U座'

fake.building_number()
# 'x座'

fake.city_suffix()
# '市'

fake.latitude()
# Decimal('-0.295126')

fake.province()
# '湖北省'
```

## pysnooper

将python程序的运行状态全部打印出来，变量变化，运行内存变化等

```shell
pip install pysnooper
```

只需要添加一个装饰器`@pysnooper.snoop()`，其他具体用法查看github地址：

https://github.com/cool-RR/PySnooper

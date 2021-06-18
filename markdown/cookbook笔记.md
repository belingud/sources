展开嵌套的序列

```python
from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    """
    可以展开多级嵌套序列，
    根据ignore_types确定忽略的数据类型
    """
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            # 返回一个生成器，如果是可迭代序列，则递归返回下一级序列
            yield from flatten(x)
        else:
            yield x
```


打印不合法的文件名

有些不合规的文件名，可以在程序中处理，使用`os.listdir()`获取并且用`open()`方法打开，但是在打印的时候会导致因为字符串的编码问题导致的异常


```python
def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')
```

> surrogateescape:
> 这种是Python在绝大部分面向OS的API中所使用的错误处理器，
> 它能以一种优雅的方式处理由操作系统提供的数据的编码问题。
> 在解码出错时会将出错字节存储到一个很少被使用到的Unicode编码范围内。
> 在编码时将那些隐藏值又还原回原先解码失败的字节序列。
> 它不仅对于OS API非常有用，也能很容易的处理其他情况下的编码错误。

```shell
>>> for name in files:
...     try:
...         print(name)
...     except UnicodeEncodeError:
...         print(bad_filename(name))
...
spam.py
bäd.txt
foo.txt
>>>
```

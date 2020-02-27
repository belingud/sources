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


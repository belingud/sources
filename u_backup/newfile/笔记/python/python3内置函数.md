逻辑判断：

- `all()`：全部值为真，返回True。空值为真值
- `any()`：任意一个值为真返回True

数学运算：

- `abs()`：绝对值
- `divmod(x, y)`：两个数字相除(x / y)，返回商和余数的元组
- `len()`：返回列表、字符串、字典、元组、set的长度，字典长度按照字典的key计算
- `max(iterable)`：返回列表、字符串、字典、元组、set中的最大值
- `min(iterable)`：返回列表、字符串、元组、元组、set中的最小值
- `pow(x, y)`：返回x的y次幂
- `range(start, stop, step)`：返回一个从start开始，步长我step的不包含stop的迭代器
- `round(x, n)`：返回x(整型、浮点数)的n位四舍五入的小数，n为0则取整
- `sum(iterable)`：返回列表、元组、set中数字的总和

类型转换：

- `bool()`：将非布尔类型转换为布尔类型，可以接受任意类型参数，在流程控制中可以不使用bool()方法，非空数据为真
- `bin(int)`：十进制转换为二进制
- `hex(int)`：十进制转换为十六进制
- `oct(int)`：十进制转换为八进制
- `float(int)`：将十进制整数转换为浮点数
- `int(obj)`：将浮点数转换为整数
- `str(obj)`：将对象转换为字符串，调用类中的`__str__()`方法，可读性好，为使用者准备，没有`__str__()`方法则调用`__repr__()`
- `repr()`：调用类中的`__repr()`方法，表示清楚，为开发者准备
- `byte(str, code)`：接受一个字符串，和目标编码格式，返回一个字节流类型
- `iter(iterable)`：接收一个列表、set、元组、字典(返回值得迭代器)、字符串，返回一个迭代器
- `dict(iterable)`：接受一个包含一个key和value的可迭代对象，返回一个迭代器
- `list(itrable)`：将元组、字典的键、set、字符串转换为列表类型，返回一个列表
- `tuple(iterable)`：将列表、字典的键、set、字符串转换为元组类型
- `set(iterable)`：创建一个无序不重复元素的集合
- `frozenset()`：创建一个无序不可变元素的集合，相对于`set()`来说，`set()`是可变的
- `complex()`：创建一个复数对象，可以是`j`或`J`
- `enumerate(seq, start=0)`：接受一个序列，返回一个枚举对象的元组，包括下标和值，start表示开始的下标
- `ord(str)`：返回ASCII对应的十进制整数
- `chr(int)`：接受0-256的整数，返回整数对应的ASCII字符
- `ascii()`：判断参数是否是ASCII编码，如果不是，输出字节码

高阶函数：

- `filter(func, iterable)`：遍历序列中的每个元素，判断每个元素得到布尔值，如果是True则留下。`func`参数对传入的数据进行判断，返回一个布尔值，True则保留在新列表，False则过滤掉。接受两个参数，一个是函数，一个是可迭代对象。

```python
import math
def is_sqr(x):
    return math.sqrt(x) % 1 == 0
tmplist = filter(is_sqr, range(1, 101))
newlist = list(tmplist)
"""
out:
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
"""
```

- `map(func, *iterable)`：处理序列中的每一个元素，得到的结果是一个list，该list元素个数及位置与原来一样，返回一个迭代器。`func`参数对传入的每一个元素进行处理，之后添加到新的序列中相同的位置。接受两个参数，一个函数地址，一个可迭代对象

```python
l4 = map(lambda x,y:(x ** y,x + y),[1,2,3],[1,2])
for i in l4:
    print(i)
""" 长度不一致，多出的元素不处理
out:
(1, 2)
(4, 4)
"""
```

- `reduce(func, iterable)`：对序列元素进行累计运算，`func`参数实现累计运算的逻辑，累加、累乘等，返回一个累计运算的结果。接受两个参数，函数名和可迭代对象

```python
from functools import reduce

def prod(x,y):
    """
    累乘运算
    """
    return x * y


print(reduce(prod, [2, 4, 5, 7, 12]))
"""
out:
3360
"""
```

序列排序：

- `reversed(sequence)`：返回一个反转序列的迭代器
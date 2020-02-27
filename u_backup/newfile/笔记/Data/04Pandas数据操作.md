<h1>Pandas数据操作<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#重复数据" data-toc-modified-id="重复数据-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>重复数据</a></span></li><li><span><a href="#映射" data-toc-modified-id="映射-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>映射</a></span><ul class="toc-item"><li><span><a href="#replace()：替换元素" data-toc-modified-id="replace()：替换元素-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>replace()：替换元素</a></span></li><li><span><a href="#map()：替换一列" data-toc-modified-id="map()：替换一列-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>map()：替换一列</a></span></li><li><span><a href="#transform()：数据转换" data-toc-modified-id="transform()：数据转换-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>transform()：数据转换</a></span></li><li><span><a href="#rename()：替换索引" data-toc-modified-id="rename()：替换索引-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>rename()：替换索引</a></span></li></ul></li><li><span><a href="#聚合操作处理异常" data-toc-modified-id="聚合操作处理异常-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>聚合操作处理异常</a></span></li><li><span><a href="#排序" data-toc-modified-id="排序-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>排序</a></span></li><li><span><a href="#数据分类/组处理" data-toc-modified-id="数据分类/组处理-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>数据分类/组处理</a></span></li><li><span><a href="#高级数据聚合" data-toc-modified-id="高级数据聚合-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>高级数据聚合</a></span></li><li><span><a href="#注意" data-toc-modified-id="注意-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>注意</a></span></li></ul></div>
---

首先将numpy，pandas导入


```python
import numpy as np 
import pandas as pd
from pandas import Series, DataFrame
```

创建一个DataFrame对象来作为示例


```python
dic = {
    "name":['lucy', 'jim', 'tom', 'rose', 'jack'],
    "python": [100,90,89,88,98],
    
}
df = DataFrame(data=dic)
```

# 重复数据

1. 利用DataFrame的duplicated方法，`duplicated(subset=None, keep='first')`，返回一个布尔类型的Series，显示是否有重复行，无重复的行为False，有重复行的为True
   - `subset=None`：用来指定特定的行，默认所有的行
   - `keep='first'`：保留第一次出现的重复项，为`last`时，保留最后一次出现，为`False`时保留全部重复行

2. 利用drop_duplicated方法，`drop_duplicates(subset=None, keep='first', inplace=False)`，移除DataFrame中的重复行
   - `subset=None`：指定行
   - `keep='first'`：删除重复项，保留第一次出现的项，为`last`保留最后一次重复项，为`False`删除全部重复项
   - `inplace`：为`False`保留副本，为`True`在原数据上修改

# 映射

映射的含义：创建一个映射关系列表，把values元素和一个特定的标签或者字符串绑定

包含三种操作：

- replace()函数：替换元素（DataFrame\Series的函数)**值的映射**
- 最重要：map()函数：新建一列(Series的函数)**列的映射**
- rename()函数：替换索引(DataFrame的函数)**索引映射**

## replace()：替换元素

**语法：**replace(self, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad', axis=None)

- to_replace：需要替换的对象，str, regex, list, dict, Series, int, float, or None
- value：替换后的值，scalar, dict, list, str, regex, default None
- inplace：是否在原数据上执行操作，bool, default False
- limit：替换次数，int, default None
- regex：to_replace的参数是否时正则，bool or same types as to_replace, default False
- method：替换方式，向前、向后替换，{‘pad’, ‘ffill’, ‘bfill’, None}
- axis：方向

**1. Series对象替换**


```python
# 获取索引为2的数据
s = df.iloc[2]
```


```python
# 单值替换
s.replace('before', 'after')
s.replace({'before': 'after'})

# 多值替换
s.replace(['before1', 'before2'], ['after1', 'after2'])  # 列表值替换
s.replace({'before1': 'after1', 'before2': 'after2'})  # 字典映射值替换
```


```python
# method填充方式
s.replace(['before1', 'before2'], method='pad')  # 向前填充
s.replace(['before1', 'before2'], method='ffill')  # 向前填充
s.replace(['before1', 'before2'], method='bfill')  # 向后填充
```


```python
# limit控制次数
s.replace(['before1', 'before2'], method='pad', limit=1)  # 只填充第一个重复项
```

**2. DataFrame对象填充**


```python
# 单值替换
df.replace('before', 'after')  # 一对一的值替换
df.replace({'before': 'after'})  # 字典映射替换关系
# 按列指定单值替换
df.replace({'column': 'before'}, 'after')  # 替换column列中的before
df.replace({'column1': 'before1', 'column2': 'before2'}, 'after')  # 替换两列中的两个元素值

# 多值替换
df.replace(['before1', 'before2', 'before3'], ['after1', 'after2', 'after3'])
df.replace({'before1': 'after1', 'before2': 'after2'})  # 字典映射的替换关系
df.replace({'before1', 'before2'}, {'after1', 'after2'})  # 后面的替换前面的两个值
```


```python
# 正则替换
df.replace(r'\?|\.|\$',np.nan,regex=True)#用np.nan替换？或.或$原字符
df.replace(regex={r'\?':None})
# value参数显式传递
df.replace(to_replace=[150,300], value=[0,0])
```

## map()：替换一列

map()函数是series的函数，一般是对DataFrame的某一列进行整体的映射

- map()可以接受一个字典
- map()可以使用lambd表达式
- map()可以使用自定义的方法
- map()可以映射新一列数据

**注意**

- map()中不能使用sum之类的聚合函数、for循环
- map(字典)字典的键要足以匹配所有的数据，否则出现NaN

**使用字典一般处理离散型的映射**


```python
# 我们用key，来表示数据中存在的需要创建映射的值，value来表示主动生成的映射值
df["column"].map({"key": "value"})  # 返回的是映射所在的新的一列，没有的数据填充NaN
```

*传入map的字典，键值比映射列的值多时，多出的值，不会报错，不会产生映射，根据这个特性，可以将所有需要映射的内容，统一整合到一个字典中*


```python
map_dic = {
    "lucy": "ming",
    "jim": "Jimmy",
    "tom": "Tommy",
    "rose": "Rosey",
    "Tim": "Timmy"
}
df["name"].map(map_dic)
```

**map中传入函数**

传入map()中的是函数名，这个函数可以显式函数，也可以是匿名函数，传入函数后会对获取的列中的元素，挨个处理。**传入函数一般处理数值型的映射**


```python
# 显式函数
def map_func(x):
    """
    获取字典值，如果没有则返回传入值本身
    """
    return dic.get(x, x)
# 获取df中的一列，使用显式函数，形成映射关系
df["name"].map(map_func)
```


```python
# 或者传入一个匿名函数
df["name"].map(lambda x: dic.get(x, x))  # 两个表达式的结果是一样
```

需要注意的是，map()函数没有`inplace`属性，不能再原数据上修改，如果需要将原数据修改，或者新增加一列来接受映射值，需要定义。


```python
df["name"] = df["name"].map(map_func)
```

## transform()：数据转换

参数：func : function, str, list or dict。可以传入函数，函数的名字，函数名的列表，或者一个用于数据处理的字典

transform输出的是原输入的DataFrame大小的，是经过了转换的DataFrame

由于transform()可以接收包含几个函数的列表，所以可以返回多于原始数据长度的的数据。

## rename()：替换索引

参数说明：

- mapper：替换所有的索引，字典
- index：替换行索引，字典
- columns：替换列索引
- level：指定多维索引的维度
- axis：指定操作数据的方向
- inplace：是否再原数据上操作

和map()函数一样，如果接收的字典参数中，右多余的数据，不会报异常。

同时，rename()支持接受多个参数，例如`rename(mapper, axis={'index', 'columns'}, ...)`


```python
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
df.rename(index=str, columns={"A": "a", "B": "c"})
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>6</td>
    </tr>
  </tbody>
</table>



```python
df.rename({1: 2, 2: 4}, axis='index')
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3</td>
      <td>6</td>
    </tr>
  </tbody>
</table>




可以使用的映射方法：

1. 使用replace()来替换值
2. 使用map()来映射列
3. 使用rename()来替换索引

# 聚合操作处理异常

describe()函数，用来展示DataFrame数据的各项指标，包括计数、均值、平均差、最大最小值、分布等指标。

与info()函数不同，info()用来查看DataFrame的状态信息，及其数据类型。


```python
df = pd.DataFrame({'categorical': pd.Categorical(['d','e','f']),
                   'numeric': [1, 2, 3],
                   'object': ['a', 'b', 'c']
                  })
df.describe()
```

默认不展示含有NaN的行，设置`include='all'`属性，可以使其全部都显示。

参数：

- percentiles : list-like of numbers, optional，0到1之间，设置展示的百分比数据
- include：默认是None，不展示有NaN的行，`all`展示所有的数据
- exclude：默认是None，设置要忽略的数据


```python
# 展示数字结果
df.describe(include=[np.number])
# 展示对象结果
df.describe(include=[np.object])
# 展示分类结果
df.describe(include=['category'])
```


```python
df = DataFrame(data=np.random.randn(1000,3), columns=list("ABC"))
```

*假定我们的目标异常数据是绝对值大于3 倍标准差的数据*


```python
# 根据每一列的标准差，对数据进行过滤
condition = (np.abs(df) > 3*df.std()).any(axis=1)
# 获取异常数据的索引，在原数据上操作，删除数据
df.drop(df[condition].index, inplace=True)
```

# 排序

DataFrame自带排序函数，根据某一列的数据排序，排序所以来的列必须是数值类型。


```python
df.sort_values("A")
```

**take()**

take()函数接收一个隐式索引列表，按照隐式索引获取数据的方式来进行排序。

同时可以使用axis来指定方向


```python
# 将df的行进行重新排序
df.take([1, 3, 2, 4, 0])
# 指定axis方向
df.take([1, 2, 0], axis=1)

# take()方法可以任意重组表格的数据，相当于拿出数据的行或列，进行重新组合成新的数据
df.take([0, 1, 0])
```

**permutation()函数**

接收一个整数数字，产生一个0到接收数字之间的全部数字随机排列的数组。可以和take函数相结合，处理随机排序


```python
np.random.permutation(10)
```




    array([0, 6, 2, 4, 7, 5, 8, 9, 3, 1])




```python
# 使用take和permutation来处理随机排序
df.take(np.random.permutation(df.shape[0]))
```

**随机抽样**

一般使用take和randint函数结合，处理随机抽样


```python
df.take(np.random.randint(0, 5, size=3))
```

# 数据分类/组处理

数据聚合是数据处理的最后一部，通常是使每一个数组生成一个单一的数值。

数据分类/组处理：

1. 分组：先把数据分成几组
2. 处理：为不同组的数据应用不同的函数以转换数据
3. 合并：把不同组得到的结果合并起来

数据分类处理的核心：

- groupby()函数
- groups属性查看分组的情况

groupby()函数的作用使使用映射或者DataFrame中一列的数据进行分组。

参数：

- by : mapping, function, label, or list of labels，传递一个分组规则
- axis: {0 or ‘index’, 1 or ‘columns’}：分组的方向
- level: int, level name：多级索引的层级
- as_index : bool, default True
- sort : bool, default True
- group_keys : bool, default True
- squeeze : bool, default False，Reduce the dimensionality of the return type if possible, otherwise return a consistent type.
- observed : bool, default False

假定我们有一组数据，蔬菜的分类和价格汇总，以这组数据为例，展示groupby()的


```python
dic = {
    "item":["萝卜","萝卜","萝卜","白菜","白菜","辣椒","辣椒","冬瓜","冬瓜"],
    "color":["white","red","green","white","green","red","green","white","green"],
    "weight":[19,30,50,34,28,89,12,56,103],
    "price":[2,3,2.5, 1,1.5, 3,3.7, 5, 4.5]
}
df = DataFrame(data=dic)
```


```python
# 返回的是一个分组完的group_by对象
res = df.groupby("item")
# 查看这个对象使用groups
res.groups
```




    {'冬瓜': Int64Index([7, 8], dtype='int64'),
     '白菜': Int64Index([3, 4], dtype='int64'),
     '萝卜': Int64Index([0, 1, 2], dtype='int64'),
     '辣椒': Int64Index([5, 6], dtype='int64')}




```python
# 获取每种菜品的总重量, 默认会得到所有能运算的列的和
res["weight"].sum()
# 使用agg函数，传入一个字典，来完成多组数据的不同聚合结果
res.agg({"price":"mean","weight":sum})  
# sum是python的内置函数，可以不是字符串类型
```

总结：数据类型是离散的可以分组，连续的数据分组没有意义

数据处理方式的分类：

1. 数据分组 groupby("item")  groupby(["item","color"])
2. 数据聚合 res.mean()  res.agg({})
3. 数据合并 pd.merge()

# 高级数据聚合

**使用groupby分组后，也可以使用transform和apply提供自定义函数实现更多的运算**

 - df.groupby('item')['price'].sum() <==> df.groupby('item')['price'].apply(sum)
 - transform和apply都会进行运算，在transform或者apply中传入函数即可
 - transform和apply也可以传入一个lambda表达式


```python
res = df.groupby("item")["weight"]
res.apply(sum)
```




    item
    冬瓜    159
    白菜     62
    萝卜     99
    辣椒    101
    Name: weight, dtype: int64




```python
# 针对某一列设计的聚合函数
# 针对所有列设计，需要考虑不同类型的问题
def function(items):
    res = 0
    for item in items:
        res += item
    return res
```


```python
res.apply(function)
```




    item
    冬瓜    159
    白菜     62
    萝卜     99
    辣椒    101
    Name: weight, dtype: int64




```python
res.transform(function)
```




    0     99
    1     99
    2     99
    3     62
    4     62
    5    101
    6    101
    7    159
    8    159
    Name: weight, dtype: int64



# 注意


- transform 会自动匹配列索引返回值，不去重
- apply 会根据分组情况返回值，去重

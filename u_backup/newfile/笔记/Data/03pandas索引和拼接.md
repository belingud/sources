# pandas索引

## 一、多层级索引

### 1. 创建多层索引

1. 隐式构造



- 读取文件是生成多层索引的DataFrame
  - pd.read_excel
  - pd.read_csv
  - pd.read_table



- 在创建DataFrame时，将index设置为product模式

```python
df = DataFrame(np.random.rand(4,2),index=[['a','a','b','b'],[1,2,1,2]],columns=['data1','data2'])
```



2. 显式构造

**MultiIndex**



- 使用数组

```python
array = [["上半年","上半年","上半年","下半年","下半年","下半年"],["北京","上海","广州","北京","上海","广州"]]
```

- 使用元组

```python
tuples = [["上半年","北京"],["上半年","上海"],["上半年","广州"],["下半年","北京"],["下半年","上海"],["下半年","广州"]]
```

- 使用product--乘积

```python
product = [["上半年","下半年"],["北京","上海","广州"]]
```

### 2. 多层级索引



除了行索引，列索引columns也能用同样的方法创建多层索引：



**Series也可以创建多层级索引，方法类似**



### 3. 多层级索引的索引和切片



#### Series操作



**对于Series来说，直接中括号`[]`和使用`.loc()`完全一样，因此，推荐使用中括号索引和切片**



索引：

```python
# 多层级索引访问的标准方式
s.loc[('index', 'column')]
# 同样也可以将要查询的表变成处理成一级索引，然后使用其他方法读取
s.loc['index'].loc['column']
# 隐式索引访问元素
s.iloc[3]
```

切片：

```python
# ('index', 'column')的方式不适合多索引的切片
s.loc[('index','column1'):[('index', 'column2')]]
# 隐式索引切片，隐式所有五十多层索引的存在，以第几列来标记元素
s.iloc[0:3]
```



#### DataFrame操作



- 隐式访问，左闭右开取键



列的访问和切片：

```python
# 列访问：可以直接使用列名来访问
df.loc[:, ('一级索引', '二级索引')]
# 列切片：通过隐式索引来切片
df.iloc[0:4]
# 不涉及赋值操作可以将其处理成单级索引，然后再访问
df['一级索引']['二级索引']
# 切片
df.loc[:, ('一级索引', '二级索引1'):('一级索引', '二级索引2')]
# 列的隐式索引切片
df.iloc[:,0:4]
```



行的访问和切片：

```python
# 行访问：通过行索引来进行访问
df.loc[('一级索引', '二级索引'), '列标签']
# 行切片：通过隐式索引来切片
df.iloc[0:4]
# 不设计赋值的操作okeyi将其处理成单机索引，然后再访问
df['一级索引', '二级索引']
# 切片
df.loc['一级索引'].loc['二级索引1', '二级索引2']
```



访问元素：



```python
# 多级index索引
df.loc[('index1', 'index2'), 'column']
```



赋值方式：



```python
# 推荐方式，用loc()的方式来访问元素，然后赋值
df['first'].loc['second', 'column']
```



## 二、索引的堆



- stack()    时将列索引转化为最内层行索引，如果想把所有的列索引转化为行索引，则需要将所有列索引通过列表转入到level中
- unstack()    是将行索引转化为最内层列索引，如果想把所有的行索引转化为列索引，则需要将所有行索引通过列表转入到level中



【小技巧】：使用stack()的时候，level等于哪一个，哪一个就消失，出现在行里；使用unstack()时，level等于哪一个，哪一个就消失，出现在列里



用level来表示索引的层级，正数表示从外到里的索引顺序，负数表示从里到外的索引顺序。



```python
# 将行索引从里到外的第二层，转化为最内层的列标签，并切片一列数据
df.unstack(level=-2).loc['conlumn']
# Series对象不支持stack()操作
df.stack(level=-1).unstack(level=0)
# df.unstack(level=-2).loc['conlumn'].stack(level=0)
```



## 三、聚合操作



- mean()    平均值
- sum()    求和
- median()    中间值
- max()    最大值
- min()    最小值
- argmax()    最大值下标
- argmin()    最小值下标
- std()    标准差
  - numpy.std()默认除以n，是有偏标准差，加入参数ddof=1得到无偏标准差
  - pandas.std()默认除以n-1，是无偏方差，加入参数ddof=0得到诱骗标准差
- prod()    元素相乘
- any()    任意
- all()    取全部



【注意】：

- 需要指定方向axis
- 和ubstack()相反，聚合的时候，axis等于哪一个，哪一个就保留（axis=0，操作行，axis=1，操作列）



### pandas和numpy中的轴——axis



stackoverflow上最高票的解释，原文地址：https://stackoverflow.com/questions/25773245/ambiguity-in-pandas-dataframe-numpy-array-axis-definition



- Use `axis=0` to apply a method down each column, or to the row labels (the index).
- Use `axis=1` to apply a method across each row, or to the column labels.



# pandas的拼接



pandas的拼接分为两种：

1. 级联：pd.concat(), pd.append()
2. 合并：pd.merge(), pd.join()


## 一、concat()


默认是纵向级联，没对齐的索引自动补全，所以pandas的级联不需要考虑形状问题，但是需要考虑索引的问题


参数：


- objs
- axis   级联方向
    - 0：保留所有的行，重复的列索引被合并，没有数据的用NaN填充
    - 1：保留所有的列，重复的行索引被合并，没有数据的用NaN填充
- join='outer'    级联方式
  - inner    交集，去除没有数据的行
  - outer    并集，保留没有数据的行
- join_axes=None    接受一个索引对象列表作为参数，级联时以join_axes的值为基准
  - 实现左右连接，生成自定义的行
- ignore_index    布尔值，是否忽略index索引，使用隐式索引代替
- keys    传递一个序列，用来生成多级索引，keys传入的值会被当做外级的索引。也可以理解为使用keys做分区处理，保留了原始索引的含义


```python
# 外连接：无论索引是否对其，都会保留在级联方向上的所有行或列
pd.concat((df1, df2), axis=1, join="outer")

# 内连接：会把级联方向上不匹配的行或列直接过滤掉
pd.concat((df1, df2), axis=1, join="inner")
```

`join_axes`传递一个列表，级联时以其值为基准，可以实现左连接、右连接

```python
# 左连接，生成的数据以左侧的DataFrame为准，空数据补NaN
pd.concat((df1, df2), join_axes=[df1.columns])
# 右连接
pd.concat((df1, df2), join_axes=[df2.columns])
```

`ignore_index`传递一个布尔值，忽略原始索引，重新分配

```python
# 忽略原始索引，重新分配，从0到n-1
pd.concat((df1, df2), ignore_index=True)
```

`keys`传递一个列表，保留原始索引含义，用keys的值来分区

```python
# 第一个DataFrame生成外级索引"first-half"，第二个生成外级索引"last-half"
pd.concat((df1, df2), keys=["first-half", "last-half"])
```

**使用append()来进行拼接**

append()函数只能沿着`axis=0`方向进行拼接

参数：

- ignore_index：布尔值，是否忽略没有数据的行
- verify_integrity：布尔值，有重复的行索引时是否报错

## merge()合并

参数：

- how：字符串，默认"inner"
    - left：只使用左侧DataFrame的索引，保留其顺序，和SQL中的左连接相同
    - right：只使用右侧DataFrame的索引，保留其顺序，和SQL中的右连接相同
    - inner：使用索引的交集，其他的直接舍弃
    - outer：使用索引的并集，没有数据的用NaN填充
- on：设置参考的列，必须使两个数据中都有的列，如果不设置on参数，也没有其他列参考，则使用交集来合并
- left_on：合并时，左侧合并参考的列
- right_on：合并时，右侧参考的列
- left_index：布尔值，是否使用左侧Datarame的索引
- right_inDex：布尔值，是否使用右侧Datarame的索引
- sort：是否给合并后的索引排序
- suffixes：处理重复的列索引，给重复的索引添加后缀，接收一个两个元素的列表

```python
# 用reset_index()把索引变成列，并重新分配索引
df.reset_index(inplace=True)  # 使用inplace参数设置在原数据上修改
# 同时可以使用drop参数来设置，是否删除原来的索引
df.reset_index(drop=True, inplace=True)
```

合并示例：

```python
pd.merge(table3, table4, on="手机型号", suffixes=["_上半年","_下半年"])
# 【注意】尽量不要使用数字的列作为合并参考列
# 删除列名为"张十三"的数据
pd.merge(df1, df2, left_on="张三", right_on="张十三").drop(labels=["张十三"],axis=1)
```

总结：

使用合并的前提：

- 参与合并的表，至少有一列可以作为合并的参考列，此两列要满足一对一、一对多、多对多关系中的一种
- 合并参考列的内容应该时离散型的，object类型的数据

**合并方式：**

1. 如果两个表中，存在一个列满足合并前提，并且两个列标签相同，可以直接合并。`pd.merge()`
2. 如果两个表中存在多个列满足合并前提，并且多列标签都相同，可以使用on来指定某一列或某几列`[col1, col2]`合并
    pd.merge(df1,df2 , on=[col1, col2], suffiexes=[控制其他列后缀])
3. 如果两个表中，存在至少一个列满足合并前提，但是没有相同的列标签，可以使用left_one、right_on来分别制定要合并的列
    pd.merget(df1, df2, left_on="", righ_on="")
4. 如果两个表中，存在至少一个相同的列标签，但是不存在满足合并前提的列，不能合并的

5. 如果两个表中，某一个或两个的行索引，满足合并前提，那么可以使用left_index=True,right_index=True来设置以行索引作为合并参考

6. how参数可以设置合并的方式
    inner  内合并 只取交集
    outer  外合并  取并集
    left   只保留第一个参数存在的数据
    right  只保留第二个参数存在的数据






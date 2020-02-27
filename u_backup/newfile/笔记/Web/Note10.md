# 函数

- 对象函数
  - 对象调用
  - 可以使用类中的所有资源
- @classmethod  类函数
  - 类调用
  - 对象调用
  - 可以使用类资源
  - 不能使用对象资源
- @staticmethod  静态函数
  - 对象调用
  - 类调用
  - 类和对象的资源都不能调用
  - 相当于寄生在我们的类上



# 数据库模型

Django中默认的数据库名字为`appname_tablename`，但是可以在模型中用元选项重命名这个表名

```python
class Game(models.Model):
    # 属性设置
    class Meta:
        db_table = table_name
        ordering = ['key_name']  #升序
        ordering = ['-key_name']  # 降序
```



# 过滤器

- filter	返回符合筛选条件的数据
- exclude    返回不符合筛选条件的数据
- all    返回符合条件的所有数据
- order_by    排序
- values    一条数据就是一个字典，返回的多个字典的列表

# 保存数据

- 创建对象时，django不会直接对数据库进行操作，对磁盘的频繁擦写，会降低程序的运行速度，django会将生成对象的SQL语句保存在缓存中，调用save方法时，才会对数据库进行操作
- 在模型类中增加类方法才能创建对象

```python
@classmethod
def create(cls, name, age):
```

# 数据查询

- get
  - get(条件)
  
  ```python
  # Django中不允许字段名中包含双下划线，它的双下划线被用来标记筛选条件中的运算符
  # 在筛选条件中如果需要有两个下划线来标记，如果只是获取字段值，需要加引号
  games = Game.object.filter(g_price__gt=50).order_by("g_id")
  ```
  
  
  
  - 双刃剑
    - 如果可以精准匹配到一个元素，可以正常使用
    - 如果没有匹配到结果，会抛出DoesNotExist
    - 如果匹配到多个结果，会抛出MultipleObjectsReturned

- first

  - 不用条件，会返回查询集中的第一个元素

- last

  - 不需要条件，返回查询集中的最后一个元素

- count

  - 返回当前查询集中的对象个数

- exist

  - 判断查询集中是否有数据，如果有数据返回True，没有就返回False

## 限制查询

django中限制查询可以用一个区间来写，前一个数字相当于`offset()`，后一个数字相当与`limit()`，下表不能为负数

```python
games = Game.objects.filter(g_price__gt=50).filter(g_price__lt=80)
# offset(2)    limit(3)
games = games[2, 5]
```



## query属性

调用query属性来输出SQL语句

```python
grades = Grade.objects.filter(Q(g_girl_nums__gt=30) | Q(g_boy_nums__gt=80))
# 打印转换的SQL语句
print(grades.query)
```



## 比较运算符

**大小写敏感的比较运算符，在前面加上`i(ignore)`就可以取消大小写敏感**

- exact    判断大小写敏感
  - filter(isDelete=False)
- contains    判断是否包含，大小写敏感
  - filter(sname__contains='赵')
- startwith, endwith    以values开头或结尾，大小写敏感
  - filter(sname__isnull=False)
- in    是否包含在范围内
  - filter(pk__in=[2, 4, 6, 8])
- gt, gte, lt, lte    大于，大于等于，小于，小于等于
  - filter(sage__gt=30)

## djange中的时间

year, month, day, week_day, hour, monute, second

```python
filter(lasttime__year=2017)
```

## 聚合函数

- Avg    平均值
- Count    统计数量
- Max    最大
- Min    最小
- Sum    求和

```python
# aggregate为获取的集合，在集合中使用聚合函数，求出最大值
Student.objects().aggregate(Max('sage'))
```

## F对象和Q对象

**F对象** 对两个属性进行比较，因为过滤条件中必须要有两个下划线来标记，才合法，在后面需要比较的属性中，没有这两个下划线，需要用到F对象，来合法化这个属性，同时，F属性也可以用来对获取的属性进行算数运算

```python
# 用F对象来比较两个属性的大小
grades = Geade.objects.filter(g_girl_num__gt=F('g_boy_num'))
# 获取属性后，通过F对象来对属性进行算数运算
grades = Grades.objects.filter(g_girl_num__gt=F('g_boy_num'+50))
```

**Q对象** 支持与或非的关键参数，用来判断过滤条件中的属性

```python
# 与：&  或：|  非：~
# 获取年龄小于25的元素
Student.objects.filter(Q(sage__lt=25))
# 获取年龄不小于25的元素
Student.objects.filter(~Q(sage__lt=25))
```


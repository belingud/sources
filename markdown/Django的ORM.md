首先这里给出一个学生model:

```python
class Student(models.Model):
    name=models.CharField(max_length=10)
    sex = models.IntegerField(choices=((1,"男"),(2,"女")),default=1)
    birth = models.DateField(null=True)
    school=models.CharField(max_length=10,null=True)
    age = models.SmallIntegerField(default=0)
    note=models.CharField(max_length=200,null=True)#备注
```

大于、大于等于:

```python
__gt  大于>        
__gte  大于等于>=

Student.objects.filter(age__gt=10)    // 查询年龄大于10岁的学生
Student.objects.filter(age__gte=10)  // 查询年龄大于等于10岁的学生
```

特别注意：这里的下划线是双下划线，下面将介绍的也都是双下划线。

小于、小于等于：

```python
__lt  小于<
__lte 小于等于<=

Student.objects.filter(age__lt=10)     // 查询年龄小于10岁的学生
Student.objects.filter(age__lte=10)   // 查询年龄小于等于10岁的学生
```

like:

```python
__exact        精确等于       like 'aaa'
__iexact       精确等于       忽略大小写 ilike 'aaa'
__contains     包含           like '%aaa%'
__icontains    包含,忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
```

in:

```python
__in

查询年龄在某一范围的学生
Student.objects.filter(age__in=[10, 20, 30])
```

is null / is not null：

```python
__isnull  判空

Student.objects.filter(name__isnull=True)    // 查询用户名为空的学生
Student.objects.filter(name__isnull=False)  // 查询用户名不为空的学生
```

不等于/不包含于：

```python
Student.objects.filter().excute(age=10)    // 查询年龄不为10的学生
Student.objects.filter().excute(age__in=[10, 20])  // 查询年龄不在 [10, 20] 的学生
```

其他常用模糊查询：

```python
__startswith 以…开头
__istartswith 以…开头 忽略大小写
__endswith 以…结尾
__iendswith 以…结尾，忽略大小写
__range 在…范围内
__year 日期字段的年份
__month 日期字段的月份
__day 日期字段的日
```

多表连接查询：

```python
 class A(models.Model):
    name = models.CharField(u'名称')
 class B(models.Model):
    aa = models.ForeignKey(A)

B.objects.filter(aa__name__contains='searchtitle')#查询B表中外键aa所对应的表中字段name包含searchtitle的B表对象。
```

返回新QuerySets的API

```
方法名                    解释
filter()            过滤查询对象。
exclude()            排除满足条件的对象
annotate()            使用聚合函数
order_by()            对查询集进行排序
reverse()            反向排序
distinct()            对查询集去重
values()            返回包含对象具体值的字典的QuerySet
values_list()        与values()类似，只是返回的是元组而不是字典。
dates()                根据日期获取查询集
datetimes()            根据时间获取查询集
none()                创建空的查询集
all()                获取所有的对象
union()                并集
intersection()        交集
difference()        差集
select_related()    附带查询关联对象
prefetch_related()    预先查询
extra()                附加SQL查询
defer()                不加载指定字段
only()                只加载指定的字段
using()                选择数据库
select_for_update()    锁住选择的对象，直到事务结束。
raw()                接收一个原始的SQL查询
```

1. filter():

filter(**kwargs)

返回满足查询参数的对象集合。

查找的参数（**kwargs）应该满足下文字段查找中的格式。多个参数之间是和AND的关系。

```
Student.objects.filter(age__lt=10)#查询满足年龄小于10岁的所有学生对象
```

2. exclude():

exclude(**kwargs)

返回一个新的QuerySet，它包含不满足给定的查找参数的对象

```python
Student.objects.exclude(age__gt=20, name='lin')#排除所有年龄大于20岁且名字为“lin”的学员集
```

3. annotate():

nnotate(args, *kwargs)

使用提供的聚合表达式查询对象。

表达式可以是简单的值、对模型（或任何关联模型）上的字段的引用或者聚合表达式（平均值、总和等）。

annotate()的每个参数都是一个annotation，它将添加到返回的QuerySet每个对象中。

关键字参数指定的Annotation将使用关键字作为Annotation 的别名。 匿名参数的别名将基于聚合函数的名称和模型的字段生成。 只有引用单个字段的聚合表达式才可以使用匿名参数。 其它所有形式都必须用关键字参数。

例如，如果正在操作一个Blog列表，你可能想知道每个Blog有多少Entry：

```shell
>>> from django.db.models import Count
>>> q = Blog.objects.annotate(Count('entry'))
# The name of the first blog
>>> q[0].name
>>> 'Blogasaurus'
# The number of entries on the first blog
>>> q[0].entry__count
>>> 42
```

4. order_by(*fields)

默认情况下，根据模型的Meta类中的ordering属性对QuerySet中的对象进行排序

```python
Student.objects.filter(school="阳关小学").order_by('-age', 'name')
```

上面的结果将按照age降序排序，然后再按照name升序排序。"-age"前面的负号表示降序顺序。 升序是默认的。 要随机排序，使用"?"，如下所示：

```python
Student.objects.order_by('?')
```

5. reverse():

reverse()

反向排序QuerySet中返回的元素。 第二次调用reverse()将恢复到原有的排序。

如要获取QuerySet中最后五个元素，可以这样做：

```python
my_queryset.reverse()[:5]
```

这与Python直接使用负索引有点不一样。 Django不支持负索引。

6.distinct()：

distinct(*fields)

去除查询结果中重复的行。

默认情况下，QuerySet不会去除重复的行。当查询跨越多张表的数据时，QuerySet可能得到重复的结果，这时候可以使用distinct()进行去重。
7. values()：

values(fields, *expressions)

返回一个包含数据的字典的queryset，而不是模型实例。

每个字典表示一个对象，键对应于模型对象的属性名称。如：

# 列表中包含的是Student对象

```shell
>>> Student.objects.filter(name__startswith='Lin')
>>> <QuerySet [<Student: Lin Student>]>
```

# 列表中包含的是数据字典

```shell
>>> Student.objects.filter(name__startswith='Lin').values()
>>> <QuerySet [{'id': 1, 'name': 'Linxiao', 'age': 20}]>
```

另外该方法接收可选的位置参数*fields，它指定values()应该限制哪些字段。如果指定字段，每个字典将只包含指定的字段的键/值。如果没有指定字段，每个字典将包含数据库表中所有字段的键和值。如下：

```shell
>>> Student.objects.filter(name__startswith='Lin').values()
>>> <QuerySet [{'id': 1, 'name': 'Linxiao', 'age': 20}]>

>>> Blog.objects.values('id', 'name')
>>> <QuerySet [{'id': 1, 'name': 'Linxiao'}]>
>>> 8.values_list()：
```

values_list(*fields, flat=False)

与values()类似，只是在迭代时返回的是元组而不是字典。每个元组包含传递给values_list()调用的相应字段或表达式的值，因此第一个项目是第一个字段等。 像这样：

```shell
>>> Student.objects.values_list('id', 'name')
>>> <QuerySet [(1, 'Linxiao'), ...]>
```
---
title: Django概述
date: ‎2019‎-‎6‎-‎21 ‏‎2:03:16
tags: 框架 Django
---



# Django概述

Django和Flask属于同一种框架，不过Django属于重量级框架封装了大量的方法，书写时代码更加简洁。Django1.11会支持到2020，首先需要安装Django

```shell
pip install django==1.11.7
```

## 创建

1. 使用命令行

创建工程：`django-admin startproject ProjectName`

创建应用：`python manage.py startapp AppName`

新创建的app需要在主框架settings.py中的`INSTALLED_APPS`中注册，在列表中追加`‘AppName’`即可。

2. 使用pycharm

项目类型选择Django

## 启动

```shell
python manage.py runserver
```

默认启动在本机的8000端口，如果要实现远程访问，需要在settings.py中设置`ALLOW_HOSTS = ["*"]`，然后在启动时添加参数。

可以添加IP和端口，或者单独添加端口，不能只添加IP

```shell
python manage.py runserver 0.0.0.0:8000
python manage.py runserver 9000
```

## 组成

目录结构树如下所示：

```shell
├── App
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── Django
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── settings.cpython-36.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

1. manage.py：环境检测和服务启动
2. AppName：目录就是我们创建的App
   - migrations：自动生成迁移文件
   - app.py：创建app配置
   - models.py：创建数据库模型
   - test.py：写测试程序
   - urls.py：注册路由，从views中导入
   - views.py：定义路由
3. 主框架
   - \_\_init__.py：传入pymysql模块，伪装成MySQLdb
   - settings.py：注册app、模板、数据库，设置路径等
   - wsgi.py：连通Client和Application
4. static：静态文件文件夹

如果使用静态文件夹，需要在settings.py里面注册静态文件目录

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

如果在pycharm里创建Django项目，会自动生成Templates文件加，用来存放模板文件，不过我们也可以自行创建文件夹标记为模板文件夹

## 数据库交互

Django是内置ORM模块的框架，也内置了迁移系统，还内置了shell，迁移系统可以和shell结合，用命令行完成更多功能。

### 迁移系统的使用

Django不需要将书库模型导入到设置里面，执行迁移命令时，会自动创建数据库

1. 生成迁移文件  `python manage.py makemigrations`
2. 执行迁移文件  `python manage.py migrate`

会在migration文件夹里面生成迁移文件，差量更新，如果需要对数据库做大量的改动，或者删除数据表，需要将迁移文件删除，然后将库中的migration表中的迁移条目删除，再进行迁移。

迁移系统用很多shell命令，用`python manage.py --help`来查看命令，一般用在测试和调试中，建完模型后测试数据库的功能，或错误复现。

### 驱动

Django默认的数据库是sqlite，如果使用sqlite，数据库配置不需要改动，可以自定义数据库名字，如果使用mysql等其他数据库需要，做相应配置，下面是mysql的三个数据库引擎比较

mysqlclient：

对python2,3都支持，但是对mysql的安装有要求，他的驱动需要获取mysql的配置文件mysql.cnf

mysql-python：

只支持python2不支持python3

pymysql：

支持python2,3，pymysql可以伪装成mysqlclient，在主框架下的\_\_init__.py里面添加代码

```python
import pymsql
pymysql.install_as_MySQLdb()
```

在框架的settings.py中配置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'HelloDjango',
        'USER': 'root',
        'PASSWORD': '000000',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

### ORM

数据库的CRUD，除了创建都是基于查询的。Django创建对象时，不会直接对数据库进行操作，对磁盘的频繁擦写，会降低程序的运行性能，Django会将生成对象的SQL语句保存在缓存中，调用save方法时，才会对数据库进行操作时。

1. create

原生Django要在数据模型中封装类方法来创建对象。

```python
@classmethod
def create(cls, name, age):
    user = UserModel.objects.create(u_name=name, u_age=age)
    return user
```

然后调用这个方法

```python
user = UserModel(u_name='Tom', u_age=23)
user.save()
```



2. retrieve

Django默认的查询管理器是`objects`，查询方法

- 过滤器
  - filter    筛选出符合条件的结果
  - exclude    筛选出不符合条件的结果

- get

  - 查询条件

  ```python
  # Django中不允许字段名中包含双下划线，他的双下划线被用来标记筛选条件中的运算符
  # 在筛选条件中如果需要两个下划线来标记，只是获取字段值需要加引号
  user = UserModel.objects.get(u_age__gt=50).order_by("u_id")
  ```

  - get是双刃剑
    - 如果精准匹配到一个元素，可以正常返回
    - 如果没有匹配到结果会跑出DoesNotExist错误
    - 如果匹配到多个结果，会抛出MutipleObjectsReturned错误
  - all
    - 返回全部查询结果
  - first
    - 不需要条件，返回查询集中的第一个元素，即第一数据
  - last
    - 不需要条件，返回查询集中的最后一个元素，即最后一条数据
  - count
    - 返回当前查询集中的对象的个数，通常配合其他查询来使用
  - exist
    - 判断查询集中是否有数据，有返回True，否则返回False

- 限制查询

  - 查询限制可以用一个区间来写，前一个数字相当于`offset()`，后一个数字相当于`limit()`，下标不能为负数

  ```python
  games = Game.objects.filter(g_price__gt=50).filter(g_price__lt=80)
  # offset(2)   limit(3)----5 - 2
  games = games[2, 5]
  ```

- query属性

  - 按照查询的结果，输出SQL语句

  ```python
  games = Game.objects.filter(g_price__gt=50).filter(g_price__lt=80)
  # 打印转换的SQL语句
  print(games.query)
  ```

- 比较运算符

  - 大小写敏感，在前面加上`i(ignore)`，可以取消大小写敏感
  - exact    精准判断，大小写敏感
    -  `UserModel.objects.filter(user__u_name__exact='tomm') `
  - contains    判断是否包含，大小写敏感
    - `filter(sname__contains='赵')`
  - startwith，endwith    以value开头或结尾，大小写敏感
    - `filter(u_name__startwith='A')`
  - in    是否包含在范围内
    - `filter(pk__in=[2, 4, 6, 8])`
  - like    像，形如，可以用正则匹配
    - `filter(u_name__like('vic*'))`   以vic开头
  - gt, gte, lt, lte    大于，大于等于，小于，小于等于
    - `filter(u_age__gt=30)`
  - order_by    通过什么排序
    - 元素前面加`-`表示逆序
    - `UserModel.objects.get(u_age__gt=50).order_by("u_id")`

- 时间参数

  - year, month, day, week_day, hour, minute, second

  ```python
  books = Book.objects.filter(b_publish_date__year=2020)
  ```

- 聚合函数

  - Avg    平均值
  - Count    统计
  - Max    最大
  - Min    最小
  - Sum    求和

  ```python
  # aggregate为获取的集合，在集合中使用聚合函数，求出最大年龄的用户
  UserModel.objects(),aggregate(Max("u_age"))
  ```

- F对象和Q对象

  - F对象，对两个属性进行比较，因为活驴条件必须有两个下划线来标记才合法，在查询中如果有两个需要比较的值，不能同时存在两个双下划线，就需要用到F对象，合法化这个属性，同时进行其他算数运算

  ```python
  # 用F对象来比较两个属性的大小
  grades = Grade.objects.filter(g_girl_num__gt=F("g_boy_num"))
  # 获取属性后，通过F对象来对属性来进行算数运算
  grades = Grades.object.filter(g_girl_num__gt=F("g_boy_num"+50))
  ```

  - Q对象，支持与或非的关键参数查询，用来判断过滤条件中的属性

  ```python
  # 与：&    或：|    非：～
  # 获取年龄小于25的用户
  UserModel.objects.filter(Q(u_age__lt=25))
  # 获取年龄不小于25的用户
  UserModel.objects.filter(~Q(u_age__lt=25))
  ```

  

3. update

   基于查询：

   1. 查询对象
   2. 修改属性
   3. 对象.save()

4. delete

   基于查询：

   1. 查询对象
   2. 查询到的对象
   3. 对象.delete

# 模型Models

## 数据模型

### 模型的字段类型

* CharField(max_length=)：字符串类型，参数为长度
* Boolean field()：布尔类型
* DateField()：日期类型，年月日
* DateTimeField()：时间类型，年月日时分秒
  * auto_now_add：第一次创建的时候赋值
  * auto_now：每次修改时候赋值
* AutoField()：自增类型
* IntegerField()：整数类型
* FloatField()：浮点数类型
* FileField()：文件类型
* ImageField(upload_to=)图片类型，存储路径，参数是路径
  * 依赖于`pillow`模块
  * 设置`MEDIA_ROOT`
* TextField()：文本类型
* DecimalField()：固定精度小数
  * max_digits：总位数
  * decimal_places：小数后几位

MEEDIA_ROOT的设置，例如存储用户头像icon，在settings.py中添加其路径：

```python
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/icons')
```

在模型中定义字段类型和限制为image文件：

```python
class UserModel(models.Model):
    username = models.CharField(max_length=32)
    # upload_to=后面是根据时间生成的路径，在静态文件文件夹里面
    icon = models.ImageField(upload_to="%Y-%M-%D")
```

当然，我们也可以不用`ImageField()`属性，自定义存储的位置，然后将路径存储到数据库中

### 模型参数

* default：默认值
* null：是否为空，存储有关，创建记录时可以不传值，用NULL填充
* blank：是否为空，校验有关，创建记录时可以为空字符串，不允许前端传空字符串，否则400
* primary_key：主键，有自增属性
* unique：唯一约束，可以有多个null

### 属性

数据模型的属性分为显性属性和隐形属性

**显性属性**包括开发主动声明的模型的属性和方法，还有从父类中继承来的属性和方法。

**隐性属性**是开发这未声明，自动生成的属性，开发者声明了就不自动生成了

例如模型的objects属性，是一个隐性属性，不需要开发者声明，自动生成，直接调用进行查询过滤，是一个manager实例，用来创建管理模型。

重写这个实例，实现对数据库数据的过滤，使返回的结果只包含没有被逻辑删除的结果。首先创建一个新的manager类，继承自Manager，重写他的`get_queryset()`方法，实现过滤功能。

```python
class LearnManager(Manager):
    # 重写查询结果集，对数据进行过滤
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_delete=Flase)
        return queryset
    def create_goods(self, g_name, g_price=10):
        goods = self.model()
        goods.g_name = g_name
        goods.g_price = g_price
        goods.save()
        return goods
```

针对数据的逻辑删除，需要在模型中定义一个删除的属性`is_delete`，删除是直接操作这个属性，我们在模型中定义这个删除的方法：

```python
class Goods(model.Model):
    is_delte = models.BooleanField(default=False)
    def delete(self, using=None, keeo_parents=False):
        self.is_delete = True
        self.save()
    # 重新定义objects为我盟的模型管理器的实例
    goods_manager = LearnManager()
```

这样我们的模型就有了一个新的模型管理器goods_manager

在views中使用管理器

```python
# 查询所有没有被逻辑删除的数据
goods = Goods.goods_manager.all()
```

## 数据关系

数据之间的管理是认为定义的，分为一对一，一对多，多对多，一对一可以通过数据表中唯一的外键来实现，一对多可以使用不唯一的外键实现，多对对则需要创建一个新的关系表，来表示两个表之间数据的关系

### 一对一

使用场景，业务拆分时，对现有的表进行拆分，或者对项目扩充，增加字段，直接操作现有表，可能会出现错误，造成无法晚会的损失，创建一个扩展的表是理想的解决方案，可以通过给外键添加唯一约束来实现一对一的关系，例如`g_foo = models.ForeignKey(User, unique=True)`，Django里面自带一个OneToOneField属性用来实现一对一的关系映射。

当操作数据库时，删除主表的内容，从表的数据也会被级联删除，删除从表数据，主表不会受影响。**谁声明的一对一关系，谁就是从表**

我们假定有两张表，一张用户表UserModel，一张用户权限表VipModel，用户表是主表，权限表是从表。声明关系语句为`v_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)`。SET_NULL可以为空。

**一对一中的属性**：主表获取从表的值，是隐形属性，获取要用模型名，根据用户表获取最后一个用户在权限表中的数据

```python
user = UserModel.objects.last()
# 对象.关联模型（模型名要小写）获取到一条vip数据
vip = user.vipmodel
```

根据从表获取主表信息是显性属性，直接按字段名就可以获取。如果要获取第一个vip的用户名，则通过权限表，获取用户表的字段

```python
vip = VipModel.objects.first()
# 对象.字段（字段是vip表中的，获取到用户对象）
user = vip.v_user
```

### 一对多

一对多的关系和一对一基本一致，使用ForeignKey来实现，默认删除主表数据，从表的数据会被级联删除，可以设置保护模式，使其不被删除。SET_PROTECT

假定我们有一个人的表，一个爱好的表，人的表是主表，定义模型

```python
# 人
class Person(models.Model):
    p_name = models.CharField(max_length=30)
    p_age = models.IntegerField(default=1)

# 爱好
class Hobby(models.Model):
    h_name = models.CharField(max_length=30)
    h_cost = models.FloatField(default=1000)
    # 一对多
    h_person = models.ForeignKey(Person, on_delete=models.PROTECT)
```

获取级联数据，Django会自动生成一个从表的`模型_set`管理器，获取从表数据通过它来获取

```python
# 从获取主，显性属性， 对象.字段名
hobby = Hobby.objects.last()
person = hobby.h_person     # 爱好对应的人
# 主获取从，隐性属性， 对象.关联模型_set  [与objects同源，所以用法也是一致]
person = Person.objects.last()
# hobby_set与objects同源，all表示所有数据
hobbies = person.hobby_set.all()  # 人对应的爱好
# 按条件获取
hobbies = person.hobby_set.filter(id=2)
```

### 多对多

表现出来的是两个数据表之间的映射，通过第三张表来体现，用`ManyToManyField`来实现，Django会自动创建第三张表关系表，关系表中会存储两张关联表的id，同样，声明关系的表是从表，并且从表不需要认为干涉。

删除数据时，会自动删除关系表中的级联关系数据

我们以用户和商品的关系，来展示级联数据的获取

```python
class UserModel(models.Model):
    u_name = models.CharField(max_length=32)
class Goods(models.Model):
    g_name = models.CharField(max_length=64)
    g_users = models.ManyToManyField(UserModel)
```

数据的操作，查询时获取的数据都是负数：

```python
# 数据查询
# 从表获取主表，是显性属性：对象.字段名
goods = Goods.object.last()
user = goods.g_user.all()
# 主表获取从表，是隐形属性：对象.从表_set
user = UserModel.objects.first()
goods = user.Goods_set.all()
# 数据改动
goods = Goods.objects.first()
user = UserModel.objects.last()
user.goods_set.add(goods)  # goods_set是自动生成的模型管理器
goods.g_user.remove(user)
goods.g_user.clear()  # 清楚所有关系数据
```

### 删除模式

在声明级联关系的字段中增加'on_delete=xxx'属性，包含以下几个值
写法例如（多对多的关系中没有on_delete属性）

```python
v_user = models.OneToOneField(UserModel, on_deletr=models.SET_NULL, null=True)
```


* models.CASECADE：默认模式，默认删除级联数据
* models.DO_NOTHING：删除关联数据，什么都不做
* models.PROTECT：保护模式，存在级联数据时，删除会报异常
* models.SET_XXX
  * SET_NULL：主表级联数据被删时置空（需要指定允许为空）
  * SET_DEFAULT：主表级联数据被删设为默认值（指定默认值）
  * SET()：删除时重新指向一个实体对象元素
    * SET(value)：删除关联的数据设为指定的值
    * SET(可执行对象)：关联值设置为可执行对象的返回值

## 模型继承

我们所创建的models模型，本身就是继承自models.Model，同样，我们也可以自己定义一个model作为基础父类，把通用的数据存储在父类的模型中。

如果直接迁移，数据库中也会直接生成父类的表，可以在基础模型中定义一个属性`class Meta:`，来抽象化基础模型。

```python
class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, autoincrement=True)
    class Meta:
        abstract = True
```

定义abstract属性之后，基础模型就不会在数据库中生成映射

## 模型和库转换

models --> db

迁移模型生成数据表

db --> models

把数据表映射到模型文件中

`python manage.py insectdb > models.py`

环境转移：

1. 导出所有依赖

`pip freeze > requirements.txt`

2. 安装所有依赖

`pip install -r requirements.txt`

# 模板Templates

## 模板文件夹

Templates文件夹存放模板文件，可以使用模板语法，**注意static文件夹里面html文件不能使用模板语法**。

Templates可以是自定义的名字，在子应用目录下需要注册，在工程目录下需要在`settings.py`里注册，然后将文件夹标记为Template Folter。

Django默认的模板配置

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    }
]
```

在views里面返回需要渲染在返回，用`render()`方法，`return render(request, 'Template.html', locals())`

## 模板语法

### 结构标签

- block
  - 定义一个块，子类标签中引用。
- extends
  - 加载父类的html文件`{% extends 'base.html' %}`
- include
  - 尽量不要使用

使用block标签来加载静态文件：

```html
{% load static %}<!--不可省略-->
<!--使用block把html代码分割，extCSS是自定义命名-->
{% block extCSS %}
    {{ block.super }}<!--继承父类block的内容-->
{% endblock %}
```



使用block + extends，化零为整，include由零化一

父标签base.html中定义一个block

```html
{% block header %}
	<h3>
        this is a header block
</h3>
{% endblock %}
```

在子标签home.html中继承

```html
{% extends 'base.html' %}
{% block header %}
{# 这是一个模板注释，网页中检查元素是不可见的 #}
{% 这是一个多行模板注释，也是不可见的。默认子标签的内容会覆盖付标签的内容，通过super来继承福标签内容 %}
	{{ block.supper }}
<h3>
    this is a child html
</h3>
{% endblock %}
```



### 变量语法

使用点语法来获取变量，在视图中返回json或者字典数据，在标签中通过key来获取。

```html
<p>{{ params }}</p>
<p>{{ param.name }}</p>
<!-- 获取列表里面的单个元素，这里是一个用户对象 -->
<p>{{ user_list.1 }}</p>
<!-- 获取对象的属性 -->
<p>{{ user_list.2.name }}</p>
<!-- 可以在试图函数里面使用__str__将对象转化为字符串 -->
```

使用点语法来引用对象方法：

```html
<p>biger:{{ dic.name.upper }}</p>
```

### 标签语法

形如`{% tag %}`的语句，就是Django的标签语法，可以实现复杂的逻辑，一些标签需要开始和结束标签

1. for循环

```html
<h3>循环取值1</h3><hr>
{% for item in person_list %}
    <p>{{ item.name }},{{ item.age }}</p>
<!-- 一个可选的empty标签，如果没有元素是展示 -->
{% empty %}
    <p>sorry,no person here</p>
{% endfor %}

<h3>循环取值2:倒序</h3><hr>
{% for item in person_list reversed %}
    <!--序号从1开始-->
    <p>{{ forloop.counter }}----->{{ item.name }},{{ item.age }}</p>
    <!--序号从0开始-->
	<p>{{ forloop.counter0 }}----->{{ item.name }},{{ item.age }}</p>
	<!-- 序号倒序 -->
	<p>{{ forloop.revcounter }}----->{{ item.name }},{{ item.age }}</p>
{% endfor %}

<h3>循环取值3：字典</h3><hr>
{% for k,v in d.items %}
    <p>{{ k }},{{ v}}</p>
{% endfor %}
```

2. if标签

```html
{% if i > 300 %}
    <p>大于{{ i }}</p>
{% elif i == 200  %}
    <p>等于{{ i }}</p>
{% else %}
    <p>小于{{ i }}</p>
{% endif %}
```

3. with标签

使用一个简单地名字缓存一个复杂的变量，当你需要使用一个“昂贵的”方法（比如访问数据库）很多次的时候是非常有用的

```html
{% with total=business.employees.count %}
	<!-- 复数显示及国际化使用pluralize -->
    {{ total }} employee{{ total|pluralize }}
{% endwith %}
```

4. csrf_token

用来标记跨站请求伪造保护

```html
{% csrf_token %}
```

5. 转义开关

作用：views.py传过来的字典值是一串html代码，默认是按字符串输出的，如果转义后则会编译成html格式在页面输出

- safe方法转义

```html
{ contents|safe }<!--添加safe完成转义，不建议-->
```

- 包裹起来转义

```html
<!--off是关闭转义，on是开启-->
{% autoescape off %}
  {{ content }}  
{% endautoescape %}
```

## 渲染模板

模板渲染返回，可以使用render方法，也可以使用**HttpResponse**来实现render的功能

```python
# 首先加载模板文件
# 返回<class 'django.template.backends.django.Template'>
template = loader.get_template('Hello.html')
# 渲染模板
result = template.render(context={"msg": "okba"})
# 用HttpResponse返回
return HttpResponse(result)
```

# 视图View

## request

request是Django框架根据Http请求报文生成的对象，包含了请求的所有信息，默认是视图函数的第一个参数

组成属性：

- path：请求页面的完整地址，不包括域名
- method：请求方法，大写，'GET', 'POST'
- GET：类字典对象，包含GET参数信息
- POST：类字典对象，包含POST参数信息，可能为空
- request：为了方便而创建，类字典对象，先搜索POST，然后GET，在高版本去除
- cookies：标准Python字典，包含所有cookies
- FILES：类字典对象，包含所上传的文件。
  - name：字符串上传文件的名
  - content-type：文件的内容类型
  - content：文件的原始内容
- META：标准Python字典，包含所有HTTP头信息，完整地址，端口，语言，编码等
  - REMOTE_ADDR
- session：可读写的类字典对象，仅当激活session时有效
- is_ajax：是否是ajax请求

几个方法：

- \_\_getitem__(key)：获取所给键的GET/POST值，先查找POST，然后GET，不存在则跑出keyerror
- has_key()：`request.POST.has_key()`，返回布尔值，是否包含所给的键
- get_full_path()：返回path，若请求参数有效，则会附带请求参数
- is_secure()：如果请求是HTTPS请求，返回True

QueryDict对象，是一个类似字典的类，被设计成可以处理同一个键有多个值的情况。它的实例是一个不可变对象，也就是说不能改变request.POST或者request.GET的值

- \_\_getitem__(key)：返回给定键的值，有多个就返回最后一个值

- get(key, default)：获取键的值，如果不存在返回默认值，类似于\_\_getitem__()

- getlist(key)：获取键对应值的列表



## 处理文件

request请求上传的文件包含在FILES里面，键来自`<input type="file" name=""/>`中的name，只在POST请求中存在，并且提交的<form>包含entype="multipart/form-data"时才生效，否则FILES只是一个空的类字典对象。

以图像为例，展示一个文件的上传和存储的过程。首先在视图函数中接受这个文件，具体实现的思路是，将文件拆分成小块的可迭代对象，然后将其写入到文件里面。

```python
from DjangoView.settings import MEDIA_ROOT
def upload(request):
    if request.method = "POST":
        username = request.POST.get("username")
        icon = request.FILES.get("icon")
        save_filename = os.path.join(MEDIA_ROOT, icon.name)
        # 用with方法来实现文件存储
        with open(save_filename, "wb") as save_file:
            # chunks 将文件拆分差成块的可迭代对象
            for part in icon.chunks():
                save_file.write(part)
                save_file.flush()
        user = User(username=username, icon=save_filename)
        user.save()
        return HttpResponse("upload file")
```



## 会话技术

### cookie

通过返回方法生成的实例来设置cookie，分为加盐和不加盐，加盐的cookie更安全

```python
resp = HttpResponse("content")
# 设置cookie
resp.set_cookie("key", "value", max_age="过期时间")
# 删除cookie
del request.COOKIES["key"]  # 删除了服务器的cookie，浏览器还有
resp.delete_cookie("key")  # 删除了对应键的值，键还存在
resp.flush()  # 删除所有cookie
# 获取cookie
request.COOKIES.get("key")
```

加盐的cookie设置获取和删除

```python
value = request.POST.get("name")
resp = HttpResponse("redirect to login")
# 设置加盐cookie，盐是一个字符串
response.set_signed_cookie("key", "value", salt="String")
# 获取加盐cookie，需要提供加的盐
value = request.get_signed_cookie("key", salt="String")
# 删除加盐cookie
resp.delete_cookie("key")
return resp
```

cookie的参数：

- key：键
- value：值
- max_age：过期时间，时间为秒
- expires：过期时间，为具体时间
- path：生效路径
- domain：生效的域名
- secure：HTTPS请求时设置为True
- httponly：用于http传输，JavaScript无法获取

### session

#### 默认

session是数据保存在服务器的回话技术，flask默认将session存在了cookie中，django默认存在了ORM中，在迁移时默认生成一张`django-session`的表，django将session持久化到了内存中。

主要有三个字段：

- session_key：唯一
- session_data：数据拼接混淆串，跟base64编码的串结合在一起
- session_expire：默认过期时间14天

```python
def login(request):
    username = request.POST.get("username")
    # 设置session
    request.session["username"] = username
    # 获取session的值
    username = request.session.get("username")
    # cookie  session 一起干掉
    request.session.flush()
    return HttpResponse("you are in")
```

你也可以在模板里面，用模板语法获取到session

```html
<h3>{{ request.session.username }}</h3>
```

#### redis

**session实现在redis中存取**借助了一个模块`pip install django-redis-sessions`，或者在下载页面下载然后`python setup.py install`，github地址：<https://github.com/martinrusev/django-redis-sessions> ，安装之后需要在settings.py里面设置如下

```python
# 引擎设置
SESSION_ENGINE = 'redis_session.session'
# 链接设置
SESSION_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': 'password',
    'prefix': 'session',
    'socket_timeout': 1,
    'retry_on_timeout': False
    }
# 如果使用远程服务器的redis
SESSION_REDIS = {
    'unix_domain_socket_path': '/var/run/redis/redis.sock',
    'db': 0,
    'password': 'password',
    'prefix': 'session',
    'socket_timeout': 1,
    'retry_on_timeout': False
}
```

集群的redis需要配置redis哨兵(Redis Sentinel)，即从服务器，也可以设置Redis Pool

```python
# 配置哨兵信息
SESSION_REDIS_SENTINEL_LIST = [(host, port), (host, port), (host, port)]
SESSION_REDIS_SENTINEL_MASTER_ALIAS = 'sentinel-master'
```

```python
# 配置redis池
SESSION_REDIS = {
    'prefix': 'session',
    'socket_timeout': 1
    'retry_on_timeout': False,
    'pool': [{
        'host': 'localhost3',
        'port': 6379,
        'db': 0,
        'password': None,
        'unix_domain_socket_path': None,
        'url': None,
        'weight': 1
    },
    {
        'host': 'localhost2',
        'port': 6379,
        'db': 0,
        'password': None,
        'unix_domain_socket_path': None,
        'url': None,
        'weight': 1
    },
    {
        'host': 'localhost1',
        'port': 6379,
        'db': 0,
        'password': None,
        'unix_domain_socket_path': None,
        'url': None,
        'weight': 1
    }]
}
```

配置好redis的连接，就可以使用redis来存session了，存取的命令没有任何的改变，Django会自动帮我们完成。

### cache

#### 默认

Django是自带缓存系统的，默认将缓存放在的了配置的数据库中，在终端命令行里面可以使用默认命令创建缓存表，`python manager.py createcachetable TableName`，会在数据库中生成一张自定义名称`TableName`的表，用来存储缓存，包含三个参数，都不允许为空

- cache_key
- value
- expires

需要在settings.py中配置缓存数据库：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'TableName',
        'TIMEOUT': '60',
        'KEY_PREFIX': 'Prefix',
        'VERSION': '1',
    }
}
```



缓存的存取：

```python
from django.core.cache import cache
resp = render(request, "person_list.html", locals())
# 设置缓存
cache.set("persons", resp, timeout=60*5)
return resp
# 获取缓存
result = cache.get("persons")
```

#### redis

用redis来实现缓存是非常理想的方式，Django中配置redis作为缓存数据库，需要用到`django-redis`，或者`django-redis-cache`模块，配置基本一直，以django-redis为例

虚拟环境输入`pip install django-redis`，然后在settings.py里面配置缓存：

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
             # "PASSWORD": "密码",
        }
    }
}
```

缓存的存取写法不变。

我们也可以使用redis实现全站缓存，来提高服务器的运行效率。 使用中间件，经过一系列的认证等操作，如果内容在缓存中存在，则使用FetchFromCacheMiddleware获取内容并返回给用户，
当返回给用户之前，判断缓存中是否已经存在，如果不存在则UpdateCacheMiddleware会将缓存保存至缓存，从而实现全站缓存

```python
# 中间件
MIDDLEWARE = [
    'django.middleware.cache.UpdataCacheMiddleware',
    # 其他中间件
    'django.middleware.cache.FetchFromCacheMeddileware',
]
```

缓存可以在单独的视图中使用

方法一：通过装饰器

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def login(request):
    username = cache.get("username")
```

方法二：通过url

```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^login/', cache_page(60 * 15)(login)),
]
```



## 分页器

Django自带了一个分页器Paginator，帮助我们实现多条数据的展示，当我们实例化一个Paginator类的实例时，需要给Paginator传入两个参数，第一个是**一个列表、元组或者查询结果集QuerySet**，第二个是**每页显示的数据，是一个整数**

Paginator类中有三个常用属性：

- count：表示所有页面对象的总数
- num_page：表示页面总数
- page_range：下表从1开始的页面范围迭代器

Page对象：Paginator类提供一个**page(number)**函数，该函数返回的就是一个page对象，number表示第几个分页，在前端显示数据时，主要的操作都是基于Page()对象的。

Page对象有三个常用的属性：

- object_list：表示当前页面上所有对象的列表
- numberv：表示当前也的序号，从1开始计数
- paginator：当前Page对象所属的Paginator对象

Page对象还拥有几个常用的函数：

- has_next()：判断是否有下一页，有就返回True
- has_previous()：判断是否有上一页，有就返回True
- has_other_pages()：判断是否有上一页或下一页，有就返回True
- next_page_number()：返回下一页的页码，如果下一页不存在抛出InvalidPage 异常
- previous_page_number()：返回上一页页码，如果上一页不存在抛出InvalidPage 异常

在view视图中，获取前端传过来的页面数据，包括页码数，每页条数，从数据库中查询数据，构建分页器，生成响应

```python
def person_list(request):
    page = int(request.GET.get("page, 10"))
    per_page = int(request.GET.get("per_page"))
    persons = Person.objects.all()
    # 构建分页器
    paginator = Paginator(persons, per_page)
    # 前一步已经生成了全部的页面，我们直接获取具体的某一页
    page_object = paginator.page(page)
    # 生成响应
    response = render(request, "person_list.html", locals())
    return response
```

在html里面接受传入的页面数据

```html
<!--用传过来的页面数据生成无序列表-->
<ul>
    {% for person in page_object.object_list %}
</ul>
```

下面展示的是页码的生成，通过判断是否有前页后页，在第一和最后页时，将按钮变为不可点击状态。用到了bootstrap和后面要讲的反向解析

```html
<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if page_object.has_previous %}
            <li>
                <a href="{% url 'two:persons' %}?page={{ page_object.previous_page_number }}&per_page={{ per_page }}"
                   aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
        {% else %}
            <li class="disabled">
                <a href="#" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
        {% endif %}
        {% for page_num in paginator.page_range %}
            <li><a href="{% url 'two:persons' %}?page={{ page_num }}&per_page={{ per_page }}">{{ page_num }}</a></li>
        {% endfor %}
        {% if page_object.has_next %}
            <li>
                <a href="{% url 'two:persons' %}?page={{ page_object.next_page_number }}&per_page={{ per_page }}"
                   aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        {% else %}
            <li class="disabled">
                <a href="#" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        {% endif %}
    </ul>
</nav>
```

## 中间件

Django中的中间件也是面向切面编程的一种，注册在settings.py中的中间件会按照顺序加载执行，是django内置的一个底层插件，本质上是MiddlewareMixin的子类，是一个类装饰器，调用`__call__`方法。

我们可以用中间件来实现类似于记录、日志、用户认证、黑白名单、优先级、拦截器、反爬虫等功能

内置的切点：

- process_request
- process_view
- process_template_response
- process_response
- process_exception
  - 界面友好化
  - 错误记录

首先创建一个middleware的package，在理编写我们的功能代码

```python
class CustomMiddleware(MiddlewareMixin):
    # 重写process_request方法
    def process_request(self, request):
        print(request.path)
    # 重写process_exception方法，出异常时重定向至首页
    def process_exception(self, request, excception):
        print(exception)
        return redirect(reverse("app:index"))
```

然后在settings.py里面注册中间件

```python
MIDDLEWARE = [
    'middleware.LearnMiddlw.CustomMiddleware',
    ...
]
```



## 返回Response

### HttpResponse

相对与HttpRequest来说，HttpRequest是Django根据request自动创建的，而HttpResponse是开发者自己创建的，我们编写的每个视图都要实例化、填充和返回一个HttpResponse对象。也就是函数的return值。

可传递的数据：

- 字符串
- 可迭代对象
- 设置头部字段

1.字符串：最简单的是传递一个定义的字符串返回

```python
response = HttpResponse("This is a string to return", content_type("text/plain"))
```

也可以将它的实例化对象看做类文件写入：

```python
response = HttpResponse()
response.write("<p>Here is a title for a web page</p>")
```

2.可迭代对象：HttpResponse会立即处理这个迭代器，并把它的内容存成字符串，最后废弃这个迭代器。比如文件在读取后，会立刻调用close()方法，关闭文件。

3.设置头部字段：可以把HttpResponse对象当作一个字典一样，在其中增加和删除头部字段。

```python
response = HttpResponse()
response["age"] = 18
del response["age"]
```

与字典不同的是，如果删除的头部字段不存在的话，会抛出KeyError，且不包含换行（CR、LF），会出现BadHeaderError异常

返回制定的数据类型`content_type`，是可选的，用于填充HTTP的`Content-Type`头部。如果未指定，默认情况下由`DEFAULT_CONTENT_TYPE`和`DEFAULT_CHARSET`设置组成：`text/html; charset=utf-8`。

`content_type`可以在MIME（多用途互联网邮件扩展）的概念中找到，他指定一个数据的类型和打开此数据的插件。

### JsonResponse

是HttpResponse的一个子类，默认`content_type = "application/json"`，传入的参数是一个字典类型

```python
# view视图中
data = {
    "msg": "ok",
    "status": 200
}
return JsonResponse(data)
```

### redirect

重定向，可以根据url、第三方路径、命名空间、对象、视图view重定向

```python
# 根据url路径
def my_view(request):
    return redirect("/index/")
# 根据第三方路径
def my_view(request):
    return redirect("heeps://www.cn.bing.com")
# 根据命名空间
def my_view(request):
    return redirect(reverse("blog:article_list"))
```

根据对象重定向，前提是在模型中定义了get_absolute_url()方法，是定义Model的对象的查看地址，主要是用在RSS与后台查看：

在模型models.py中：

```python
class Post(models.Model):
	title = models.CharField('标题',max_length=200)
	slug = models.CharField('slug',max_length=255,blank=True)
	summary = models.TextField('摘要',blank=True)
    body = models.TextField('正文')

	def get_absolute_url(self):
        return reverse('post_view',args=[self.slug])
```

视图views.py中：

```python
def my_view(request):
    obj = MyModel.objects.get(...)
    return redirect(obj)
```

扩展：在模板中使用get_absolute_url()方法，在模板中生成标签时，使用这个方法而不用指明url路由的信息

```html
<a href="{{ object.get_absolute_url }}">{{ object.name }}</a>
```



### 正向解析，反向解析

正向解析就是根据url地址访问页面

反向解析就是根据命名空间定向到url

根路由Project/urls.py里面

```python
urlpatterns = [
    url(r'app/', include("app.urls"), namespace='app')
]
```

应用路由app/urls.py里面

```python
urlpatterns = [
    url(r'^index/', views.my_view, name='index')
]
```

在模板里面使用反向解析：

```html
<!--反向解析到应用app的index路由中-->
<a href="{% url "app:index" %}">
```


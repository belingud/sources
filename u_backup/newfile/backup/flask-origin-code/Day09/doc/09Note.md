

### Web框架之Django

- Django
  - Flask和Django属于同一种框架
  - Flask是轻量级的
  - Django是重量级的
- Tornado
  - Tornado轻量级
  - 也可以像Django，Flask一样作为一个常规Web服务器
  - 可以处理高并发，性能比Django和Flask好
  - 也可以作为客户端使用， 作为中继客户端，向主服务发送请求
  - MCS(Middle, Client, Server)



### HelloDjango

- 安装，首选安装稳定的版本，1.11会支持到2020年
  - pip install django==1.11.7
- 创建项目
  - 使用命令行创建项目比用pycharm创建项目少templates目录，不过可以在pycharm自行创建，右键将其设为templates folds类型
  - 用命令行创建项目
    - 创建工程
      - `django-admin startproject ProjectName`
    - 创建应用
      - `python manage.py startapp AppName`
  - PyCharm
    - 项目类型选择django
- 启动
  - `python manage.py runserver`
    - 默认启动在本机的8000端口上
  - 也可以添加参数
    - ip:port
      - `python manage.py runserver 0.0.0.0:9000`
    - port
      - `python manage.py runserver 9000`



### Django项目的组成

- manager.py：环境检测和服务启动
- AppNmae目录：我们创建的app
  - migrations：在迁移数据库中会自动生成里面的文件，不需要做改动
  - apps.py：创建app的配置
  - models.py：创建数据库模型
  - tests.py：写测试程序
  - urls.py：注册路由，可以将路由注册在主框架下面，具体方法是将`AppName`目录下的views.py导入，`views.route`导入这个接口
    - `urlpatterns = [url(r'^home, views.home)]`
  - views：定义路由功能，函数名传入到url里面
    - Django不像Flask，请求request不是全局可调用，函数需要传入request，才能接受到请求
    - 接口回传数据需要用到`HttpResponse()`方法，括号里传入字符串
    - 渲染页面需要用到`render()`方法，返回值包括request, templates_name, context, context_type, status, useing

- 主框架下的文件
  - \__init__.py：传入pymysql模块，将其伪装成MySQLdb
  - setting.py：注册app，注册模板，数据库设置，路径设置，以及其他系统相关设置
  - wsgi.py：不需要变动



### Django中的迁移系统

- Django内置ORM模块
- Django内置迁移系统
- 迁移系统使用
  - django不需要将数据的模型Models导入到设置里面，在执行迁移命令时，会自动创建
  - 首先生成迁移文件
    - `python manage.py makemigrations`
  - 执行迁移文件
    - `python manage.py migrate`

### Django中内置shell

- Django中的shell拥有更多的功能，可以用`python manager.py --help`来查看命令
- 一般用在测试和调试中，建完模型后测试数据库的功能，或者错误复现

### MySQL驱动

- mysqlclient
  - python2,3都能支持
  - 对mysql安装有要求，需要获取mysql的配置文件mysql.cnf
- mysql-python
  - python2支持
  - python3不支持
- pymysql
  - python2,3都支持
  
  - pymysql可以伪装成mysqlclient
  
  - ```python
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



### 新建Application

- 指令
  - `python manage.py startapp AppName`
- 创建完的应用首先要注册
  - 在settings中的`INSTALLED_APPS`中
    - 使用应用名字可以注册，在后面追加`‘AppName’`就可以添加
- 如果不注册
  - 项目主体就不知道新模块的存在，导致models，admin，apps系统都不能探测到



### 模板templates

- 每个App中可以存在自己的模板路径
  
  - 不需要额外声明，注册
- 也可以不写在App中，可以交给工程管理
  
  - 需要在settings中进行注册
  
  - ```python
    TEMPLATES = [
        {
        'DIRS': [
                os.path.join(BASE_DIR, 'templates')
            ],
    	}
    ]
    ```



### 数据ORM的简单使用

- 数据的CRUD
- 创建
  - 正常创建对象
  - 对象.save()
- 删除
  - 基于查询
  - 查出来的对象
  - 对象.delete
- 修改
  - 基于查询
    - 查出来的对象
    - 修改对象属性
    - 对象.save()
- 查询
  - 查询入口
  - objects
  - 复数
    - all()
  - 单数
    - get
    - first

```python
# 从GET请求中获取grade_id
grade_id = request.GET.get("grade_id")
# 依照接受的参数，在Ｇｒａｄｅ表中查询得到对象gragde
grade = Grade.objects.get(pk=grade_id)
# 调用类方法实现功能
grade.save()
```





### homework

- 使用django实现上周作业



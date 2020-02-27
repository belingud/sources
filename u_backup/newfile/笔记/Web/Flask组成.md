

# Flask组成

## Flask四大内置对象

1. request
2. session
3. g
4. config或app
   - 就是当前运行的项目
   - 获取当前运行的app的配置



## 基本组成

1. config配置项
   1. 注册app
   2. 配置数据库
   3. SECRET_KEY
2. 模型
   1. 定义一个模型的类
   2. 可以将对需要模型完成的功能封装
   3. 需要初始化
3. 定义路由（接口）
   1. 使用装饰器
   2. 函数（FBV模型）
4. 配置run
   1. debug
   2. host
   3. port
5. static
   1. 可以直接访问
6. templates
   1. 模板，html文件，用来渲染返回

##  config配置项

### app

```python
from flask import Flask
# 注册app
app = Flask(__name__)
```

### 数据库

```python
from flask_sqlalchemy import SQLAlchemy
# SQLALCHEMY_DATABASE_URI顺序为“数据库+数据库驱动://用户名:密码@host:port/数据库名字”
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:000000@localhost:3306/DatabaseName"
# 数据库的修改确认，定为False，否则会提示错误
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 创建数据库对象，来实现数据库的操作
db = SQLAlchemy(app)
```

### SECRET_KEY

可以设置一个SECRET_KEY来加密数据

```python
app.config["SECRET_KEY"] = "123"
```

### SQLAlchemy

引入SQLAlchemy作为ORM，相当于翻译器，将python代码转化为数据库操作，需要对他进行配置

首先是引入：

```python
db = SQLAlchemy(app)
```

然后是配置：

```python
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hello.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:000000@localhost:3306/FlaskModel"
# 没有这一项配置会有警告提示
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```

### 跨域请求

使用flask-cors模块来解决跨域请求问题

安装：`pip install flask-cors`

在\_\_init__.py中配置跨域

```python
from flask_cors import CORS
CORS(app)
```

### flask中的csrf

flask默认csrf关闭，可以在config.py中将其打开

```python
CSRF_ENABLED = True
```



## 模型

### 定义一个模型的类

```python
class Book(db.Model):
    # 主键自增属性
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    price = db.Column(db.Float, default=100)
    # 外键也要定义数据类型，外键链接的是具体的字段
    type = db.Column(db.Integer, db.ForeignKey(Type.id))
```

### 封装方法

一般将重复调用或者属于某个模型的方法封装在模型中，层级更加分明，使用更方便，简化代码

### Flask数据库操作

创建映射表：

```python
db.create_all()
```

删除表：

```python
db.drop_all()
```



在模型类中封装save方法：

```python
# 使用SQLAlchemy作为ORM
def save(self):
    db.session.add(self)
    # 默认是支持事务的
    db.session.commit()
```

### 字段类型和约束

- 类型
  - Integer
  - Biginter
  - String
  - Text
  - Date
  - Time
  - Boolean
- 约束
  - primary_key
  - autoincrement
  - unique
  - nullable
  - default
  - index
  - ForeignKey

### 数据库的迁移

迁移是指将模型转变成数据库中的表，使用flask-migrate模块，可以结合flask-script使用，script模块可以给项目定制脚本，设定运行参数，代替在run里面的设置

首先安装：

```shell
pip install flask-migrate
# 结合flask-script使用
pip install flask-script
```

配置：

```python
# 绑定app和db
migrate = Migrate(app, db)
# 给app添加迁移命令
manager = Manager(app)
manager.add_command("db", MigrateCommand)
```

使用命令迁移数据库模型：

```python
pythom manager.py db init  # 初始化
python manager.py db migrate -m 'Version'  # 生成迁移文件，-m 制定版本信息
python manager.py db upgrade  # 迁移
python manager.py db downgrade  # 降级
```



## 路由（接口）

```python
# 路由的地址为login，支持GET，POST方法
@app.route('/login/', methods=["GET", "POST"])
# 接口方法名为login
def login():
```

**Flask中的request是全局可用的，不需要传入路由**

### 路由操作数据库

查询方法：

- get
- filter
- order_by
  - 必须先调用
- limit
- offset
  - offset和limit先执行offset
- paginate
- 条件
  - \>    \_\_gt_ _
  - <    _\_lt__
  - ==
  - \>=
  - <=
  - in_
  - like
  - startswith----前面加i忽略大小写
  - endswith

操作命令例如：

```python
# 获取Student数据并分页显示，默认10条一页
pagination = Student.query.paginate()
```

**使用文本化SQL**

使用 `text()` 方法可以用文本化的方式执行查询，使得语法更灵活，`filter()`和`order_by()`都可以使用。

```python
from sqlalchemy import text
# 在view视图中调用
filter(text("id<3"))
```

保存：`object.save()`



### 方法

#### 模板渲染

render_template()：

```python
@app.router('index')
def index():
	return render_template('xxx.html', pagination=pagination, msg='hahahaha')
```

重定向redirect()：

结合反向解析url_for()

```python
# login是定义的路由接口
return rerdirect(url_for("login"))
```

#### 设置cookie

定义一个Response用做返回，用Response调用set_cookie()方法，代码实现：

```python
response = redirect(url_for('mine'))  # 重定向
response.set_cookie("key", value)
return response
```

#### 设置session

导入flask中的session，通过键值对方法设置session，例如：

```python
session["u_name"] = user.name
session["u_icon"] = user.icon
```

#### 从提交的数据中获取文件

- view试图获取文件

获取用户上传的文件，存储在服务器，然后在数据库中存储路径

```python
icon = request.files.get("icon")
# 设置路径并存储头像
ext = "." + icon.filename.split(".")[-1]
save_path = "PATH" + u_name + ext
icon.save(save_path)
```

- 模板中上传

在input中需要定义一个属性，向浏览器声明文件传输的操作

示例：

```html
<input method="post" action={{ url_for("user_blue.register") }} entype="mulitipart/form-data">
```

#### token

首先要安装flask-caching模块，设置radis作为缓存数据库，在第三方库里面配置。

```python
from flask_caching import Cache
cache = Cache(config={
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": "redis://:PASSWORD@localhost:6370/1"
})
TOKEN_TIME_OUT = 60*60*24
# 在init_ext(app)中注册
def init_ext(app):
    cache.init_app(app)
```



在view试图中使用token，设置

```python
token = uuid.uuid4().hex
cache.set(token, user.id, timeout=TOKEN_TIME_OUT)
```

获取：

```python
cache.get("token")
```

使用flask-httpauth来进行flask的auth认证，查看博客：

<https://segmentfault.com/a/1190000011277435>



#### g对象

g对象是一个可以全局（应用内）传递参数的对象，将需要携带的数据，作为自己本身的属性进行传递，生命周期只有一个request的长度。

```python
from flask import g
g.msg = "balabala"
```

在html中接受g

```html
<h1>{{ g.msg }}</h1>
```



## Blueprint

将项目按照整体配置和具体业务进行拆分的写法，实现高内聚、低耦合，便于管理。

### 项目目录

#### \_\_init__初始化模块

- 创建Flask对象`app = Flask(__name__, template_folder='../templates')`
- 初始化配置`app.config.from_object(envs.get(env))`
- 初始化扩展库`init_ext(app)`
- 加载中间件`load_middleware(app)`
- 加载路由`init_blue(app)`
- `return app`

#### config或setting系统设置模块

- 配置环境，直接定义成类，选择环境时获取属性即可
- 配置数据库，根据环境选择不同的数据库
- 配置其他项（KEY, DEBUG, TESTING, SQLALCHEMY_TRACK_MODIFICATIONS）

#### views试图函数模块

- 将子试图里面的路由集初始化

```python
def init_blue(app):
    app.register_blueprint(blueprint=user_blue)
    app.register_blueprint(blueprint=movie_blue)
```



#### extension第三方库模块

- 配置ORM

- 配置缓存
- migrate迁移命令

```python
db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": "redis://:000000@127.0.0.1:6379/1",
})
def init_ext(app):
    db.init_app(app)
    migrate.init_app(app)
    cache.init_app(app)
```

#### middleware中间件

首先引入一个概念，面向切面编程，在Flask中的中间件是用装饰器来实现的，可以在不修改源代码的情况下，对既有程序添加功能

- 请求接受前
  - befor_request接受request数据
- 请求接收后
  - after_request接受request和response数据
- 捕获异常
  - errorhandler接受request和exception数据

```python
def load_middleware(app):
    @app.before_request
    def app_before():
        pass
    @app.after_request
    def after(resp):
        print(resp)
    @errorhandler(500)
    def error500(exce):
        return "跳转到首页"
```



### App目录结构

#### models模型模块

- 定义抽象基类继承自`(db.Model)`，其他模板直接继承自它，然后设置属性`__abstract__ = True`使其不再数据库中生成映射。可选
- 模型定义的属性就是数据表的字段，设置约束就是数据表的约束
- 封装方法

#### views视图模块

首先定义路由集，其他的路由函数都用这个视图集装饰，在根路由中注册路由集后就可以直接按照url访问

```python
# url_prefix是路由前缀，url访问的地址
user_blue = Blueprint("user_blue", __name__, url_prefix="/user")
```

定义路由时，用其进行装饰：

```python
@user_blue.router("/idnex/", method=["GET", "POST"])
def index():
    return "Hello World"
```

## flask-RESTful

flask-RESTful是flask的API写法，和Django中的Django-REST-framework类似，属于CBV模型，通过函数试图模型来实现接口功能，实现继承和方法的封装重写，python里的类继承是写的最好的，API式的开发方式，充分发挥了这个优点。

flask-RESTful也是flask的一种，模块拆分和配置和flask大致相同，首先是写好配置文件settings.py, ext.py, 根views.py，跟前文的配置类似。区别在于，因为是API式的写法，在views.py中注册路由，是注册的router.py中定义的Api，例如：

在app/views.py中定义资源类：

```python
class AppResource(Resource):
    # 重写post方法
    def post(self):
        data = {
            "status": 201,
            "msg": "add ok"
        }
        return data
```



在app/router.py中定义Api路由：

```python
from flask_restful import Api
# prefix前缀，这个api的的根
app_api = Api(prefix='/app')
# AppResource是在views中定义的资源类
app_api.add_resource(AppResource, '/')
```



在Project/views.py中注册：

```python
def init_app(app):
    # 在flask中需要用init_app()来初始化路由
    app_api.init_app(app)
```



在app的router.py中注册的路由，加上一个`prefix='/app'`的参数，就是url的路径前缀，例如 http://127.0.0.1:5000/app/ ，在资源类中同意接受通过这个url传入的请求，通过继承和重写，实现定制功能。

### models

引入一个flask中的密码校验机制，generate_password_hash和ckeck_password_hash方法。输入密码每次输出的密文都不同，同时可以通过check_password_hash方法来验证密码。

实现原理大致为，先对密码进行hash加密，再将加密后的hash字符串拼接一个定制的字符串，验证是去除定制的字符串，然后将接收的密码hash，比较两个hash。

models的定义方式就是flask中定义模型的方式

### router

用来定义api路由，并用add_resource()方法添加到views.py中的资源类中。

```python
blogs_api = Api(prefix="/blogs")
blogs_api.add_resource(BlogsResource, "/")
blogs_api.add_resource(BlogResource, "/<int:pk>/")  # 传入参数时，经过这个路由
```



### views

#### 定义资源类

在views.py中定义一个资源类，继承自Resource，Resource重写了父类MethodView中的`dispatch_request`方法，获取并校验请求方法名，并根据方法名分发请求。

资源类中重写方法名函数，实现功能的定制。

例如：

```python
class UsersResource(Resource):
    # 重写post请求的处理方法
    def post(self):
        args = parse.parse_args()
        action = args.get("action")
        if action == "register":
            return self.do_register()
```



在view中根据需要传入的参数，添加请求参数规则

```python
from flask_restful import Resource, reqparse
# 首先声明请求转换器
parse = reqparse.RequestParser()
# 添加请求参数规则
parse.add_argument("username", required=True, type=str, help="username can`t be blank")
```

添加转换器后获取参数，从转换器中获取区别于之前的request获取

```python
# 直接获取
username = request.form.get("username")
# 通过过滤规则
args = parse.parse_args()
# 获取html中form表单的数据，如果客户端不是html也能提交表单数据
action = args.get("action")
```





#### 格式化数据

格式化数据是**flask_restful**里面的一个写法，定义一个fields字典格式的格式化模板，对获取和输出的数据进行格式化操作，省去了手动改变格式的麻烦。

```python
# 定义一个格式化数据的模板
data_fields = {
    "id": fields.Integer(attribute="number"),
    "name": fields.String(default="Tom")
}
# 定义一个要返回的信息模板
return_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    # 级联数据写法
    "data": fields.Nested(student)
}
```



输出格式化的数据可以使用两种方法：

1. 装饰器

在请求方法函数前面加上`@marshal_with(return_fields)`，输出的数据会自动根据return_fields格式化

2. 调用marshal方法

在return的data中用marhsal方法来格式化数据，同样需要传入一个模板

```python
data = {
    "status": 201,
    "data": marshal(data, data_fields)
}
return data
# 或这直接输出
# return marshal(data, data_fields)
```

3. 输出字典格式数据

如果元数据不是字典格式，就需要将其写成字典格式，重复使用体验不佳，视情况而定。

```python
data = {
    "status": 201,
    # to_dick是已经封装好的方法
    "data": [book.to_dict() for bood in books]
}
```

用装饰器给请求的处理方法添加方法和属性。定义一个方法，实现对传入请求处理方法的参数进行处理。

例如：

```python
# 定义装饰器
def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.form.get("token")
        if not token:
            raise "error"
        user_id = cache.get(token)
        user = User.query.get(user_id)
        g.user = user
        return func(*args, **kwargs)
    return wrapper
```

在资源类中装饰请求方法函数

```python
class BlogResource(Resource):
    @login_required
    def post(self):
        return "ok"
```




























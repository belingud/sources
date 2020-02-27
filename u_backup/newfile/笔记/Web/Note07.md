

## 移动端接口编写

- http协议
- 编写路由
  - 浏览器 （客户端一种）CS/BS
  - B(Browser)是一个C(Client)子集
- 服务器返回数据
  - 网页数据 html
    - 浏览器对用呈现
  - JSON数据
    - ajax  javascript发送请求的一种方式
    - requests  Python的一个请求库
    - 各种平台有各种平台的请求方式
- 为移动端编写接口非常简单
  - 接口地址是什么
    - 全路径：https://www.lte.ink/user/login
    - 相对路径：/user/login
  - 接口需要什么参数，返回什么格式的数据
    - 参数根据业务场景
    - 大部分JSON数据



### 接口文档

- 接口请求方式

  - POST

- 请求参数

  - username     用户名    长度最大32    必须值      mlfc
  - password     密码     长度最大32    必须值      mlfc

- 响应

  - status  状态码    200   
  - msg    描述   
  - data   数据 
    - 用户信息
    
    - 示例

```python
{
	status: 200,
	msg: 'ok',
	data: {
		id: 1,
		username: 'Rock',
		password: 'rock1204',
		age: 18,
		hobby: 'coding, learn, sleep'
	}
}
```

### RESTFul

- 软件架构设计思想
- CS，客户端和服务端模型中
- 表现层状态转换
  - 主语 （资源）
  - **URI 每个URI代表一种资源**
  - 资源展现给我们的形式就叫做表现层
  - **HTTP请求谓词** 通过HTTP的请求谓词来实现表现层转换
- 重要概念
  - URI
  - HTTP请求谓词
    - POST
    - GET
    - PUT
    - DELETE
    - DETCH
  - JSON



## Flask-RESTful

- 轻量级的RESTApi插件
- marshal_with(是一个类)
  - 装饰器
  - 参数接收模板
  - 将返回的数据进行格式化
    - 数据内容如果比模板多，结果会自动删除多余的数据
    - 数据内容如果比模板少，结果会自动进行填充
- 核心
  - 请求转换    输入
  - 输出格式化    输出

### marshal_with()实现对象转json

**实现步骤：**

1. 通过给请求处理方法添加装饰器实现

- 首先根据数据库定义的`model`格式，创建一个对应的**json对象**作为需要返回的json数据的**模板**，例如写一个book类的模板：

```python
book_fields = {
    "bname": fields.String,
    "bprice": fields.Float,
    "id": fields.Integer,
    "bauthor": fields.String, # bauthor在book的model中没有定义
}
```

- 通过装饰器`@marshal_with()`导入`book_fields`json对象

```python
from flask_restful import marshal_with, fields, marshal
@marshal_with(book_fields)
def post(self):  # post是客户端发送请求的方式
    bname = request.form.get("bname")
    bprice = request.form.get("bprice")
    book = Book(bname=bname, bprice=bprice)
    # 保存成功
    return book
	# 或者不用装饰器，在返回值里面直接将对象和模板传入marshal()
    # return marshal(book, book_fields)
```

2. 将marshal方法应用到需要生成的数据中

- 首先根据需要传出的json数据，创建一个json模板
- 然后在数据data里面，将对象json化，直接传出data，可以附带状态信息

```python
from flask_restful import fields, marshal
def post(self):  # post是客户端发送请求的方式
    bname = request.form.get("bname")
    bprice = request.form.get("bprice")
    book = Book(bname=bname, bprice=bprice)
    if book.save():  # save是在book类里面定义的方法，用来存储book对象
        data = {
            "msg": "save success",
            "status": 201,
            # 格式化数据     ①参数  ②模型
            "data": marshal(book, book_fields)
        }
        return data
```





### MTV

- Template最先继承
- Model 也能继承
- Views 也能继承



### Views分类

- 使用函数实现了视图函数
  - FBV
  - Function Based View
  - 基于函数的视图函数
- 使用类实现了数图函数
  - CBV
  - Class Based View
  - 基于类的视图函数



### 列表生成式

- 生成一个列表



### 装饰器

- 装饰器实现
  - 直接使用函数
    - 函数套函数
  - 使用类进行实现
    - 实现call魔术方法



### CookBook

- <https://python3-cookbook.readthedocs.io/zh_CN/latest/#>
- 优先看
  - 1, 7, 8, 9
- 次看
  - 2
- 其余看心情



### homework

- 追上昨天的代码
- 总结问题
  - 记录下来问题
- 搭建FlaskAPI项目
  - 实现注册，登陆








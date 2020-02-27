# flask_RESTful的基本用法

### 数据安全

flask里的内置函数，可以直接实现密码的加密和校验

- generate_password_hash
  - 输入相同，每次输出的密文输出都不一样
- check_password_hash
  - 调用函数可以直接进行密码验证

实现的原理

- 先将密码进行hash
- 再将hash拼接一个随机数
- 验证
  - 去掉随机数
  - 密码生成hash
  - 比较hash



### 程序的异常

- 异常产生
  - raise
  
    - ```python
      @property
      def password(self):
          # 访问密码时抛出异常
          reise Exception("not be accessed")
      ```
  
  - assert
- 处理异常
  
  - try...except
- 主动抛异常场景
  - 自己封装框架
  - 封装工具类给别人使用

### Flask-RESTful

```python
，即给数据库中的字段定义映射，或叫设置别名# 添加参数的一般写法
parser = reqparse.RequestParser()  # 定义一个传入的参数
parser.add_argument("title", type=str, required=True, help="please add your title", action='append', dest='public_name', location=['form', 'values']) # location中后面的参数先显示
```

- 输入
  - reqparse.RequestParser()
    - 对参数进行处理
    - 参数获取
    - 获取校验
      - 参数名  
      - 类型限制  type
        - 两个类型 int 和 str
      - 错误提示  help
      - 是否必须   required
        - 默认下，arguments 不是必须的，在请求中提供的参数不属于 RequestParser 的一部分的话将会被忽略。设置 `required=True`来调用`add_argument()`
      - 隐私别名   dest
        - 设置的别名，将别名传出，隐藏数据库中的字段名
      - 参数来源   location 后面的参数先显示
        - form
        - args
        - heads
        - cookies
        - values![1558615802217](/home/vic/.config/Typora/typora-user-images/1558615802217.png)
        - json
      - 参数数量，多个参数值   action
        - append追加参数
        - store储存参数
- 转换输出格式的方法
  - 将对象转换成JSON（dict）
  
  - marshal_with  装饰
  
  - marshal 函数
    
    - 先写好传出数据的模板
    - 将数据和模板传递进来
    
### 需要输出的模板

- 字典（将模板定义为字典，输出的字典会被自动转化为json数据）
  - key 就是json中key
  - value 就是`fileds.XXX`
- fields
  - `attribute`指定映射关系
    
  - 格式化的时候，会默认根据字典中的key去数据中查找，指定 `attribute=“xxx”`之后，会根据 attribute去查找。可以实现给传出的字段设置别名(xxx)

```python
student_fields = {
	"name": fields.String(attribute=b_name)  # b_name是数据库中设置的字段名
}
```


   - default 默认值
       - 如果不存在字段或内容，返回只为`null`，可能会影响前端的功能实现，设置默认值可以解决这个问题


```python
student_fields = {
	"unknown": fields.String(default="")  # 设置默认值为空字符串
}
```

- fields.Nested 
  - 嵌套字段
  - 对象嵌套
  - 可以自动处理单个对象和列表对象

```python
student_fields = {  # 定义student输出数据的模板
	"name": fields.String(attribute=b_name)  # b_name是数据库中设置的字段名
}
retuen_fields = {
    "msg": fields.String,
    "status": fields.Integer,
    # 将student模板通过Nested方法传入到return模板中，将将传入到data键的数据格式化，即下文中的"data": student
    "data": fields.Nested(student_fields)  
}
```

引入`marshal_with()`后，将`matshal_with()`作为方法的装饰器使用，将输出结果格式化

```python
from flask_restful import Resource
class LearnResoure(Resource)
	@marshal_with(return_fields)
	def get(self):
        # 省略实现方法
        data = {  # 需要返回的数据
            "msg": "ok",
            "status": 200,
            "data": student,
        }
        return data
```

- fields.List
  
  - 解决列表型数据（旧写法）

`"data": fields.List(fields.Nested(student_fields))`



### fileds

- 继承自Raw
  - 属性
    - default 默认值属性
    - attribute 
  - 方法
    - format 将传入的数据格式化
    - output 
- String
  - format 
    - 转换成str
    - text_type
- Integer
  - format
    - int
- Boolean



## 封装方式

- 函数 静态方法 将需要实现的方法写在函数里面，在需要的地方调用函数实现功能，实现代码复用
- 类的继承   创建一个父类`BaseResource`，在父类里面定义类方法，在继承自他的子类中，都可以使用这个方法，这种方式方便在父类的属性也可以被继承
- 装饰器，同样是创建一个函数方法，不过将其作为装饰器使用将要实现功能的方法`function`传入装饰器，为方法添加功能

```python
# 定义一个装饰器
def login_required(fun):
    def wrapper(*args, **kwargs):
        # 省略需要给函数添加的功能
        return fun(*args, **kwargs)
    return wrapper
```

```python
# 在实现的方法中添加装饰器的功能
@login_required
def post(self):
    # 处理传入的数据
    data = {
        "msg": "ok",
        "status": 200,
        "data": blog
    }
    return marshal(data, return_fields)
```





### flask中

- GET参数获取方式
  - `request.args`
  - `query_string `
  - `query_params`
  - 在所有的请求中都可以直接使用
  - 想拿这个数据可以用通用写法 `request.args`
- POST参数获取方式
  - request.form
  - **POST，PATCH，PUT参数都是使用form获取**



### homework

- 自己安装一个postman

- 自己实现密码数据安全策略
  - 生成密码密文每次不一样
  - 还可以自己实现密码验证
- 用户分级
  - 超级管理员
- 有兴趣的
  - 用户角色
    - 比如贴吧为准
      - 超级管理员
        - 自带
      - 吧主
        - 谁创建的贴吧
      - 小吧主
        - 吧主任命
      - 用户
        - 自己来的
        - 用户注册


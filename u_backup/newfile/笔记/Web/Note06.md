# Day06



### 算法

- 摘要
  - 通常做数据安全
  - 数据验证
  - 实现
    - md5
    - sha
  - 特性
    - 单向不可逆
    - 不管输入多长，输出长度都是固定的
    - 杂凑算法，指纹算法
    - 算法公开
- 编码
  - 为了解决原生不被支持的语言或者符号
  - 通常用在数据数据传输过程中
  - 偶尔会被用在加密过程中
  - 实现
    - base64
    - urlencode
  - 特性
    - 可逆
    - 算法透明
- 加密算法
  - 对称加密
    - 密钥
      - 一把
    - 密钥既可以加密，也可以解密
    - 实现
      - DES，AES
    - 特性
      - 加密效率高
      - 相对安全
        - 密钥一旦泄漏，数据也会泄漏
  - 非对称加密
    - 密钥
      - 一对
      - 公钥
      - 私钥
    - 特性
      - 公钥加密，只有私钥能解密
      - 私钥加密，只有公钥能解
      - 私钥自己保留，公钥暴漏给外界
      - 安全性高
      - 效率偏低
    - 实现
      - PGP
      - RSA（支付宝，微信）

### url_for

- 反向解析
- 动态获取地址

- url_for("视图函数名字" )
- 可以视图函数上的路由
  - 带参
    
    - url_for("视图函数名字", key=value, key=value)
    
      - ```python
        action="{{ url_for("users_blue.login") }}
        ```
    
        
  
- static
  - url_for("static", filename="xxx")
  
  - ```python
    @app.route("/static/<path:filename>")
    def static(filename):
    ```
  
- 在app中是以上所说
  
- 在蓝图中前面要拼接蓝图的名字
  
  - url_for("蓝图名.函数名")



### 模型

- 模型默认一定会在数据库中产生映射
- 如果模型不想在数据库中产生映射
  - 需要模型是抽象的
  - 抽象的模型不会有具体的实例
  - \__abstract__ =True



### 文件上传

- 文件不能一次传输
- 需要打碎，然后再拼装
- 中间需要对应的规则
  
  - enctype
  
  - ```HTML
    <form enctype="multipart/form-data">...</form>
    ```



### PyCharm快捷键

- 重构
  - shift + f6
  - 会将所有关联资源自动修改



### Flask返回Json数据

- jsonify
  - 可以直接接收字典
















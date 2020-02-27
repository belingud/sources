# Day16



### DRF

- 官网
  - <https://www.django-rest-framework.org/>
- 中文版文档
  - <https://q1mi.github.io/Django-REST-framework-documentation/>
- 特性
  - 可浏览API
  - 提供丰富认证
  - 支持数据序列化
  - 可以轻量嵌入，仅使用fbv
  - 强大的社区支持
- 基于Python打造的实现了RESTApi风格重量级框架
- HelloDRF
  - 安装
    - pip install djangorestframework
  - 创建
    - serializers
      - 序列化模块
      - 模型和json转换的
    - views
      - viewsets
    - urls
      - router
    - 配置
      - settings中的 INSTALLED_APPS
  - 启动测试
    - 直接实现了数据的增删改查
    - 可浏览模式
    - 也可以使用API形式，json格式展示





### PUT&PATCH

- put和patch通常都是用在更新上
- put
  - 全量更新
  - 必须提供所有需要的字段，哪怕没有修改
- patch
  - 差量更新
  - 只需要提供修改了的字段就ok



### 序列化  serializers

- serializers.Serializer
  - 手动书写字段
  - 实现抽象方法
    - create
    - update
  - 手写麻烦
    - 开发中也不咋用
- 序列化器使用
  - model -> dict  -> json
  - 使用模型对象去构建序列化对象
    - 获取序列化对象的data
  - json -> dict -> model
  - 使用dict数据去构建序列化对象  XXXSerializer(data=dict)
    - 先验证  is_valid
    - 再save
  - errors属性
    - 当验证不通过的时候，使用errors属性
- serializers.ModelSerializer
  - 继承自 serializers.Serializer
  - 最省事
  - 开发中最喜欢用
- serializers.HyperLinkedModelSerializer
  - 最智能
  - 配置也麻烦
  - 开发中基本不用





### 双R

- request
  - django中的request只能接收GET，POST参数，PUT，PATCH的参数未做处理，需要自己手动处理
  - DRF中对Request进行重构， request.data
    - data可以接收POST，PUT，PATCH 参数
- response
  - Django中TemplateResponse的子类
  - 可以根据请求客户端的不同来返回不同的内容



### status

- 实现代码友好化



### views转换 Wrapping

1. @api_view装饰器
   1. 直接添加不能使用，需要添加允许请求的方法列表
   2. 将django的request转换成了restframework中的request
   3. 原来的HttpResponse可正常兼容
   4. 使用新的Response可以根据客户端自动转换显示结果
2. 继承APIView
   1. 可兼容原有代码
   2. APIView继承自View





### 抽象方法

- 父类中没有实现的方法
- 子类必须实现的方法
- 方法定义中没有编写任何逻辑，直接抛出 NotImplementedError 异常的









### 接下来安排

- Django 
  - DRF
  - 定时任务
  - 日志
- 项目
  - 前后端分离
  - VUE + DRF
  - VUE + Flask-RESTful
  - 部署，上线
- Tornado
- 考试



### homework

- 使用DRF做一个登陆，注册
- 使用HTML进行注册，登陆
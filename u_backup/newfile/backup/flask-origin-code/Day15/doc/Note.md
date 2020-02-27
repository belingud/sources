# Day15



### 视图函数

- FBV
- CBV
  - class
  - 可以被继承



### HelloCBV

- 首先在视图函数中创建View的子类
  - 在类中进行请求函数的编写
  - 根据请求方法的名字编写的
- 注册路由
  - View.as_view()



### View

- 调用顺序
  - as_view
    - 判定
      - as_view传递进来的关键字参数不能是请求方法的名字
      - as_view传递进来的参数必须是类中既有的属性
    - 定义view 函数
      - 创建自己的对象
      - 只要支持get请求就支持head请求
      - 调用 dispatch
  - dispatch
    - 根据请求方法名字小写去既有请求方法列表中判定
      - 如果不存在，直接返回http_method_not_allowed
      - 如果存在，会根据请求方法去获取对应的属性，
        - 属性如果不存在也返回http_method_not_allowed
        - 属性存在返回正常的属性值
      - 调用属性（属性一定是函数）
  - http_method_not_allowed
    - 直接返回HttpResponse
  - _allowed_methods
    - 返回列表
    - 列表中存的是允许请求的方法名字
  - options
    - 是一个请求方法
    - 默认所有的CBV支持options请求

- 属性和方法
  - \__init__
  - as_view
  - dispatch
  - http_method_not_allowed
  - options
  - _allowed_methods
  - http_method_names



  ### 类视图CBV流程

  - as_view
    - view
      - diaptch
        - 根据请求方法名字分发




### TemplateView

- 它有三个爸爸
  - TemplateResponseMixin
  - ContextMixin
  - View
- TemplateResponseMixin
  - 属性
    - template_name
    - template_engine
    - response_class
    - content_type
  - 方法
    - render_to_response
    - get_template_names
  - 作用
    - 将上下文内容渲染到模板中
- ContextMixin
  - 属性
    - 无
  - 方法
    - get_context_data
  - 作用
    - 获取上下文数据
- View
  - 属性
    - http_method_names
  - 方法
    - as_view
      - view
    - disptach
    - http_method_not_allowed
    - options
  - 作用
    - 用来分发请求
- TemplateView到底做了什么？
  - 分发了请求
  - 实现了get
  - 获取了上下文
  - 渲染成响应
    - 获取模板
      - 需要开发者配合





### ListView

- 有两个爸爸
  - MultipleObjectsTemplateResponseMixin
    - 它有一个爸爸
      - TemplateResponseMixin
        - 属性
          - template_name
          - template_engine
          - response_class
          - content_type
        - 方法
          - render_to_response
          - get_template_names
    - 属性
      - get_template_suffix
    - 方法
      - get_template_names（重写）
  - BaseListView
    - 它有两个爸爸
      - MultipleObjectsMixin
        - 它有一个爸爸
          - ContextMixin
            - 方法
              - get_context_data
        - 属性
          - allow_empty
          - context_object_name
          - model
          - ordering
          - page_kwargs
          - paginate_by
          - paginate_class
          - paginate_orhans
          - queryset
        - 方法
          - get_queryset
          - get_ordering
          - paginate_queryset
          - get_paginate_by
          - get_paginator
          - get_paginate_orhans
          - get_allow_empty
          - get_context_object_name
          - get_context_data
            - 重写的
      - View
    - 属性
      - 无
    - 方法
      - get
        - 默认支持get请求
    - 执行流程
      - 看get中的调用
    - 完整流程
      - url -> as_view
      - as_view -> dispatch
      - dispatch -> get
      - get -> get_queryset
        - 根据queryset属性和model属性进行查找
        - get_ordering 
        - get_allow_empty
      - get_queryset -> get_context_data
        - get_paginate_by
        - get_context_object_name
        - 向context中注入数据
      - get_context-> render_to_response
        - context 包含了上面的数据



### 权限

- 用户
- 用户组
- 权限
- 用户组权限（关系表）
- 用户权限表 （关系表）
- 用户用户组表 （关系表）





### 后台管理

- 功能强大
- 自定义难度高
  - 可以使用插件，实现样式自定义
  - xadmin
  - admin-suit
  - django-jet



### homework

- 实现点击列表中的item，跳转到详情
  - DetailView




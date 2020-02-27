# Day17



### APIView

- 继承自View
- 入口函数
  - as_view
    - queryset检测
      - 不要直接操作queryset, 直接操作会发生多个请求之间的数据错乱
      - 推荐使用 all 或者 get_queryset
    - 调用父类中的as_view
      - 参数检测
      - 定义闭包函数
      - 记录数据
      - dispatch
  - dispatch
    - 重写方法
    - 做了一个Request转换（初始化）
    - 之后进行整体初始化
      - 格式化后缀
      - 内容决策
      - 版本决策
        - 强制升级
        - 推荐升级
        - 没有升级
      - 执行认证
      - 检查权限
      - 节流，限流
    - 根据请求方法进行分发
    - 如果上述处理过程中出线异常，异常并不会直接被抛，异常会被捕获
    - 提供异常策略
    - 最终对响应进行统一处理
    - 最后返回

### APIView源码

- 属性
  - args
  - authentication_classes
  - content_negotiation_class
  - format_kwargs
  - headers
  - kwargs
  - metadata_class
  - parser_classes
  - permission_classes
  - renderer_classes
  - request
  - response
  - schema
  - settings
  - throttle_classes
  - versioning_class
  - http_method_names
- 方法
  - as_view
  - allowed_methods
  - default_response_headers
  - http_method_not_allowed(重写)
  - permission_denied
  - throttled
  - get_authentication_header
  - get_parser_context
  - get_renderer_context
  - get_exception_handler_context
  - get_view_name
  - get_view_description
  - get_format_suffix
  - get_renderers
  - get_parsers
  - get_authenticators
  - get_permissions
  - get_throttles
  - get_content_negotiator
  - get_exception_handler
  - perform_content_negotiation
  - perform_authentication
  - check_permissions
  - check_object_permissions
  - check_throttles
  - determine_version
  - initialize_request
  - initial
  - finalize_response
  - handle_exception
  - raise_uncaught_exception
  - options 



### APIView源码调用

- as_view
  - 定义view
  - dispatch
- dispatch
  - initialize_request
    - get_parser_context
    - get_parsers
    - get_authentitors
    - get_content_negotiator
  - default_response_headers
  - initial
    - get_format_suffix
      - kwargs上获取的
      - key是settings中配置的FORMAT_SUFFIX_KWARG
    - perform_content_negotiation
      - get_renderers
      - get_content_negotiator
    - determine_version
      - versioning_class
    - perform_authentication
      - request.user
      - 执行完认证了？
      - user是一个使用property修饰的函数
        - 获取request._user
        - 属性不存在则执行认证过程
        - 遍历认证器
        - 调用认证器的方法 authenticate
        - 如果认证成功会返回一个元组（user，auth），user和auth会被存到request上
        - 如果认证出现异常，或者所有认证器都没有陈宫，会直接进入 _not_authenticated
      - get_authenticators获得的认证器
    - check_permissions
      - get_permissions
      - 迭代
      - 如果没有权限，会permission_denied
        - 直接抛异常 让程序终止
      - 什么情况算是有权限
        - 所有的权限器都无返回，has_permission都返回true
    - check_throttles
      - get_throttles
      - 节流器会有 allow_request方法
        - 返回True代表允许
        - 返回False代表不允许
          - 不允许就会Throttled
          - 就是抛异常



### generics

- GenericsAPIView
  - 继承
    - APIView
  - 属性
    - filter_backends
    - lookup_field
    - lookup_url_kwarg
    - pagination_class
    - queryset
    - serializer_class
  - 方法
    - get_queryset
    - get_object
    - get_serializer
    - get_serializer_class
    - get_serializer_context
    - filter_queryset
    - paginator
      - 使用property修饰
    - paginate_queryset
    - get_paginated_response
- CreateAPIView
  - 继承
    - GenericAPIView
    - CreateModelMixin
  - 方法
    - post
      - create
- ListAPIView
  - 继承
    - GenericAPIView
    - ListModelMixin
  - 方法
    - get
      - list
- RetrieveAPIView
  - 继承
    - GenericAPIView
    - RetrieveModelMixin
  - 方法
    - get
      - retrieve
- DestroyAPIView
  - 继承
    - GenericAPIView
    - DestroyModelMixin
  - 方法
    - delete
      - destroy
- UpdateAPIView
  - 继承
    - GenericAPIView
    - UpdateModelMixin
  - 方法
    - put
      - update
    - patch
      - partial_update
- ListCreateAPIView
  - 继承
    - GenericAPIView
    - ListModelMixin
    - CreateModelMixin
  - 方法
    - post
      - create
    - get
      - list
- RetrieveUpdateAPIView
  - 继承
    - GenericAPIView
    - RetrieveModelMixin
    - UpdateModelMixin
  - 方法
    - get
      - retrieve
    - put
      - update
    - patch
      - partial_update
- RetrieveDestroyAPIView
  - 继承
    - GenericAPIView
    - RetrieveModelMixin
    - DestroyModelMixin
  - 方法
    - get
      - lretrieve
    - delete
      - destroy
- RetrieveUpdateDestroyAPIView
  - 继承
    - GenericAPIView
    - RetrieveModelMixin
    - UpdateModelMixin
    - DestroyModelMixin
  - 方法
    - get
      - retrieve
    - put
      - update
    - patch
      - partial_update
    - delete
      - destroy





### mixins

- CreateModelMixin 
  - 函数
    - create
    - perform_create
    - get_success_headers
- ListModelMixin （复数）
  - 函数
    - list
- RetrieveModelMixin  （单数）
  - 函数
    - retrieve
- UpdateModelMixin （单数）
  - 函数
    - update
    - perform_update
    - partial_update
- DestroyModelMixin  （单数）
  - 函数l
    - destroy
    - perform_destroy



### viewsetsl

- ViewSetMixin
  - 属性
    - action
    - basename
    - description
    - detail
    - name
    - suffix
  - 方法
    - as_view
    - initialize_request
    - reverse_action
    - get_extra_actions
    - get_extra_action_url_map
- ViewSet
  - 继承
    - ViewSetMixin
    - APIView
- GenericViewSet
  - 继承
    - ViewSetMixin
    - GenericAPIView
- ReadOnlyModelViewSet
  - 继承
    - GenericViewSet
    - ListModelMixin
    - RetrieveModelMixin
- ModelViewSet
  - 继承
    - RetrieveModelMixin
    - ListModelMixin
    - UpdateModelMixin
    - CreateModelMixin
    - DestroyModelMixin
    - GenericViewSet





### homework

- 只有登陆的用户可以访问动物列表
- 哪一个用户创建动物，动物就归属谁








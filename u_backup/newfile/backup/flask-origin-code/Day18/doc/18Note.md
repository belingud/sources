# Day18





### 认证权限

- 用户，动物
- 动物管理
- 登陆的用户查看动物列表
- 动物谁创建的，就是哪个用户



### 超管

- 动物查询
  - 首先必须登陆
    - 默认查询显示登陆的用户的所有动物
    - 超级管理员登陆，显示所有的动物
- 实现
  - 先去修改用户，添加超管
  - 查询过滤

### 规划流程

- 删除动物
- client -> delete （http://localhost:8000/app/animals/1/?token=xxxxx）
- urls - > views
- views -> as_view
  - 各种检测
  - dispatch
    - initialize_request
    - initial
      - 后缀检测
      - 内容决策
      - 
      - 版本决策
      - 认证
        - authenticate
      - 权限
        - has_permission
      - 节流
        - allow_request
    - 根据请求方法分发
      - get
      - post
      - put
      - patch
      - delete (删除)
        - destroy
          - get_object
            - get_queryset
            - filter_queryset
            - check_object_permission
        - perform_destroy





### 需求转换

- 用户注册，登陆
- 动物添加，查询



### 元编程

- 动态底层创建
- CookBook



### 认证和权限判定流程

- 认证和权限是两码事
- 认证
  - 用户身份识别
- 权限
  - 不同的用户身份拥有不同的操作权限
- perform_authentication
  - 从APIView获取认证器（可以是元组或列表） （内部存的是类）
  - 生成认证器对象（列表生成式）（内部存的是类的对象）
  - 执行认证的时候遍历认证器对象
    - 调用认证器的  authenticate 方法
    - 认证成功返回 用户, 令牌  元组
      - 认证成功返回的用户和令牌会被存储到request上
    - 认证失败默认不返回就ok
- check_permissions
  - 从APIView获取权限检测器 （可以是元组或列表） （内部存的是类）
  - 生成权限检测器对象（列表生成式）（存储的是类的对象）
  - 执行权限检测的时候遍历权限检测器
    - has_permission
    - 返回True有权限
    - False没有权限





### isinstance

- 是不是某个类的实例
- isinstance(object, class)
  - 判定object是不是class的实例





### homework

- 巩固知识
- 写一个搜索（任意模型的搜索）
- 添加一个节流








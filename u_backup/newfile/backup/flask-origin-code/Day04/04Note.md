# Day04



### 业务分析

- 登陆，注册，个人中心
- 围绕用户
  - 用户模型
- 登陆路由
  - 展示页面
  - 处理登陆的页面
- 注册路由
  - 展示页面
  - 处理注册的页面
- 个人中心路由
  - 展示页面
    - 需要判定用户是否为登





### 模型过滤

- filter之后对象类型是  BaseQuery
- BaseQuery可以链式调用
  - Student.query.filter(xxx).filter().filter().filter()



### MTV

- View
  - route
    - 请求方法
    - 请求路径
    - 反向解析  url_for()
  - views
    - 双R
    - 会话技术
- Template
  - 模板语法
  - 和static区别
    - static可以直接使用
  - template需要路由渲染
- Model
  - ORM
  - 数据存储
  - 数据查询
  - 数据删除
  - 数据更新



### 扩展

- 内置扩展
  - 蓝图
    - flask-blueprint
    - 用来拆分路由器的
- flask-script
  - flask脚本
  - 安装
    - pip install 
  - 初始化
    - app
  - 使用



### Property

- 装饰器
- 将函数转换成属性使用
- 可以实现对属性操作的动态介入





### 收入

- 正规收入
  - 工资
  - 投资
- 非正规收入
  - 灰产
    - 游走在法律边缘
  - 黑产
    - 走在违法的道路上








# Day05



### 开发环境

- 开发环境
- 测试环境
- 演示环境
- 生产环境



### 扩展库

- 迁移
  - 可以自动将模型变成数据库中的表
- 实现
  - flask-migrate
- 使用过程
  - 安装
    - pip install flask-migrate
  - 配置
    - 绑定app和db
    - 创建一个Migrate对象，传递app和db进去
    - 如果和flask-script一起使用
      - 在manager对象上添加指令   add_command("db", MigrateCommand)
  - 具体使用
    - 首次使用需要初始化
      - python manage.py   db  init
    - 如果模型有变更，生成迁移文件
      - python manage.py db  migrate
    - 将迁移文件映射到数据库中
      - python manage.py db upgrade
      - 后悔药
      - python manage.py  db downgrade



### Flask 四大内置对象

- request
- session
- g
  - global 全局
  - 帮助我们实现全局数据共享
    - 生命周期  在单次请求中
- config 或者 app
  - 就是当前运行的项目
  - 获取当前运行的App的配置
    - 应该是存在价值和意义的



### 钩子函数

- 编程模型
  - OOP
    - 面向对象编程
  - POP
    - 面向过程编程
  - IOP
    - 面向接口编程
  - AOP
    - 面向切面编程
- 动态介入到既有流程中
- 重要概念
  - 切点
    - 请求前
    - 请求后
    - 请求异常
  - 切面
    - 请求前
      - request
    - 请求后
      - request
      - response
    - 请求异常
      - exception
      - request
- Flask中就叫做钩子（切点）
- 蓝图和app上都有钩子函数
  - app上的钩子优先级更高
  - 蓝图只能处理本蓝图内容的信息



### 缓存

- 减少磁盘io可以大幅度提升服务器性能
- 实现
  - flask-cache
  - flask-caching



### 版本号

- xxx.yyy.zzz
- xxx 大版本更新，不兼容更新
- yyy 小版本更新，添加或修改部分功能，可兼容
- zzz bug版本，优化版本，修bug



### 电脑核心组成

- 处理器 CPU
  - 针对于家用，性能基本过剩
- 主板  
  - 匹配CPU存在
- 内存 
  - 足够大  
  - 目前标配 16G
- 显卡
  - 机器学习
- 磁盘 
  - 机械硬盘
  - SSD
    - SATA
    - M.2



### homework

- 知识梳理
- 手动操作一下缓存
  - 自己去存
  - 自己去取






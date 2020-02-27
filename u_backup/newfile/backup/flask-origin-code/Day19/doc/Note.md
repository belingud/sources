# Day19



### DRF

- 节流



### Throttling

- BaseThrottle
  - allow_request
    - 抽象方法
  - get_ident
    - 获取唯一标识
  - wait
    - 等待时间
- SimpleRateThrottle
  - 继承
    - BaseThrottle
  - 属性
    - THROTTLE_RATES
    - cache
    - cache_format
    - duration
    - history
    - key
    - now
    - num_requests
    - rate
    - scope
    - timer
  - 方法
    - get_cache_key
    - get_rate
    - parse_rate
    - allow_request
    - throttle_success
    - throttle_failure
    - wait
  - 调用
    - allow_request
      - 需要很多参数
      - 了解参数的初始化
        - rate
        - scope
      - parse_rate
        - rate格式
          - 100/m
          - 60/minute
      - get_cache_key
        - 确定我们缓存的标识







### getattr

- 获取指定对象上的属性
  - getattr(object, key, default_value)
  - getattr(func, key, default_value)
- 函数上的装饰器属于函数的属性



### Django中Request

- request.META和request.environ 一样



### 代理

- 普通代理
  - 速度快，价格便宜
  - 可以被捕获到真实ip
- 高匿代理
  - 隐藏真实ip
  - 速度慢，价格贵

### 刷题

- <https://leetcode.com/> 



### 面试题

- <http://exercise.acmcoder.com/online/online_judge>  赛码



### 公司组成

- HR（人力资源部）
  - 招聘
  - 员工关系
  - 薪酬制定
  - 社保公积金
- 前台（行政部门）
  - 打杂的
  - 收发快递，接待访客
  - 水电网，场地
  - 办公物品采购
- 技术
  - 后端
    - Java
    - PHP
    - Python
    - GO
    - Node JS
  - 前端
    - Web
    - Android
    - IOS
  - 测试
  - 运维
  - 美工
  - 产品
- 财务
  - 绩效合算
  - 出纳
  - 审计
- 产品线（核心）
- 运营推广
  - 提升影响力
    - 让别人知道
      - 地铁
      - 百度
      - 社区
  - 口碑
- 销售
  - 线上销售
    - 网咨
    - 电销
  - 线下销售
    - 合作
- 售后
  - 维护产品正常状态
  - 维修产品
- 法务
  - 法务冲突
  - 规则制定







### 工资发放

- 全额按国家制度，政策发放
- 基本工资+绩效



### 公司发展

- 拿自己的钱去创业
- 拿别人的钱完成自己的理想
- 发展过程
  - 天使轮（种子）（100w-2000w）
  - A （500w-2000w）
  - B  （1000W-）
  - C
  - D
  - E
  - IPO (上市)



### 收入

- 工资
- 理财，投资
  - 基金
    - 一带一路
      - 定投
    - 5G
  - 股票
- 私活
- 灰产
- 黑产



### 产品研发

- 后端
  - 标配两个人
    - 会有一个技术强（主程）
    - 另外一个一般的（打手）
  - 开发语言
    - Java
    - PHP
    - Python
    - GO
    - Node JS
    - C/C++
- 前端
  - Web
    - 技术
      - VUE
      - React
    - 标配一个人
  - 移动
    - Android
      - 标配一个
      - Java + xml
      - Kotlin + xml
    - IOS
      - 标配一个
      - OC
      - Swift
- 测试
  - 黑盒
    - 功能测试
  - 白盒
    - 用代码测试
- 运维
  - 标配一个
  - 可能由后端兼职
- UI
  - 标配一个
  - UD，UE
- 大团队
  - 架构师
  - 技术经理
  - 团队组长
  - DBA
  - 网络安全
- 时间积累
  - 数据分析工程师
  - 人工智能



### 开发流程

- 





### 开发阶段






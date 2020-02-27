



### 模板渲染

- 在模板中使用在视图函数中传递过来的数据
- 在视图函数中通过关键字参数的形式传递数据
- 特性
  - 兼容性很强
  - 数据多传了，少传了都不会报错



### 模板语法

- 变量  {{ var }}
- 标签 {% tag %}
  - block
    - 块
    - 坑
  - extends
    - 继承，扩展
    - 子模板可以填充父类中的块，坑
    - 没有填充的块会被自动优化掉
  - block + extends (更推荐)
    - 化整为零
    - 特性
      - extends继承
        - 父模板没有要求
      - block
        - 首次出现的block
          - 代表一种规划
        - 第二次出现的block
          - 代表规划的填充
        - 第三次出现的block
          - 代表对规划的填充
          - 默认会覆盖第二次的填充
          - 获取父模板中的内容使用{{  super() }} 
        - block 中可以嵌套 block，继续规划
  - include
    - 包含
    - 将其它html包含到自己的页面中
    - 体现了一种由零聚一的思维
  - 宏定义
    - macro
    - {% marco  XXX(params)  %}...{% endmacro %}
    - 定义好的宏可以被调用
    - macro可以被其它html导入
    - {% from xxx import  yyy %}
    - {{ xxx() }}  调用

### for

- {%   for  item in   iters  %}... {% endfor %}
- 循环中存在循环变量存储（循环器）  loop
  - index
  - revindex
  - first
  - last



### if

- 条件分支
- {% if exp %}...{% endif %}
- {% else %}
- {% elif  exp %}





### PyCharm

- control + alt + l
  - 快捷格式化代码





### ORM

- Object Relational Mapping
  - 对象关系映射
- 将数据库转换为面向对象的操作
- 通过操作对象就可以实现数据的增删改查
- 如何理解ORM
  - ORM就是一个翻译机
- 优点
  - 开发效率高
  - 可以对接多种数据库（移植性高）
  - 易于理解，便于维护
    - 将数据转换为面向对象编程
  - 实现了防SQL注入
- 缺点
  - 执行效率低
    - 因为需要将对象的操作转换为数据库的SQL
  - 对于复杂操作可能没有支持



### MySQL数据类型

- 文本（字符串）
- 数字
- 时间



### 模型

- 定义模型
- 无非就是增删改查
  - 存储
    - 创建一个对象
    - 通过db.session.add
    - 最后记得commit
  - 删除
  - 修改
  - 查询
    - 类名.query.操作
      - all 拿所有  默认返回是  list
      - filter()  过滤 
        - 过滤条件
          - 类名.属性名  操作符   值
          - 类名.属性名.操作符 值
        - 返回BaseQuery
        - 可以继续all
    - get(主键)





### SQL漏洞

- select * from user where username=Tom and password=110;
- select * from user where username=root and password=110 or id=1;



### homework

- 对接用户注册，登陆
  - 注册
    - 创建用户
  - 登陆
    - 条件查询用户




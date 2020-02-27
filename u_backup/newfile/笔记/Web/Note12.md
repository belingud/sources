### 模板

- 结构标签
  - block
  - extends
  - include
     - 尽量不要使用
- block + extends
  - 化整为零
- include
  - 由零化一



### url匹配规则

- 自上而下进行匹配
  - 按照列表索引进行升序匹配
- 没有最优匹配的概念
  - 只要匹配到就可用的就结束
- 注意
  - 结束了记得写斜线
  - 如果有斜线还冲突，记得添加结束符号
  - 是按照正则表达式来进行匹配



### 获取url中的参数

- 和正则一样
- 第一种
  - 使用 () 获取数据
  - ( ) 中书写规则
  - 路由中存在参数获取，要求视图函数要添加对应的参数获取
    - 一 一对应
  - 参数是位置参数，和名字无关，和顺序（位置）有关
  - 大层面是路径参数
- 第二种
  - (?P<name>) 可以根据name获取参数
  - 参数是关键字参数
  - 大层面来说，依然是路径参数



### 反向解析

- 准备工作
  - 在根urls中，include时添加namespace
```python
url(r'teo/', include('teo.urls', namespace='teo'))
```
  - 在子urls中，添加name属性
```python
url(r'^login/', views.login, name='login'),
```
- 使用
  - python中
```python
redirect(reverse("namespace:name"))
```
  - 模板中
```html
{# 将form表单重定向到teo里的login路由里面ji #}
<form action="{% url 'teo:login' %}" method="post">
```
- 如果有参数
  - 位置参数
    - python
```python
reverse('namespace:name', args=(value, value, value...))
```
   - 模板中  {% url "namespace:name"  value  value ... %}
        - 关键字参数
      - python写法
```python
reverse("namespace:name", kwargs={key:value, key:value})
```
   - 兼容写法
```python
reverser("namespace:name", args=(value, value...)) 不推荐
```
   - 模板中
```html
{% url "namespace: name"  key=value key=value... %}
```




### json

- 互联网交互的轻量级数据格式
- key-value
- 类型分类
  - JSONObject
     - {}
  - JSONArray
     - []
- value 可以是一个对象
- python内置 json模块
  - 将json数据转换成 dict
    - loads
  - 将dict转换成json
    - dumps



### 小知识点

- 函数的默认参数
  - 如果是数据容器，默认值是None
- 如果直接传递容器，实际对应的容器的地址
  - 会操作同一个容器
  - 出现数据错乱


### 算法可视化

- <https://visualgo.net/zh>



### 观测内存分配

- <http://www.pythontutor.com/visualize.html#mode=edit>
- copy, deepcopy
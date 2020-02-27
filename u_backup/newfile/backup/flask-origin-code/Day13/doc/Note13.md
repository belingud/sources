# Day13



### session

- session默认存储在内存中
- 在Django中被持久化到了数据库中
  - 主要有三个字段
    - session_key
      - 唯一
      - 生成的字符串
    - session_data
      - 我们的数据拼接混淆串
      - 最后base64编码的数据
    - session_expire
      - 过期时间，默认14天
- Flask中默认将所有的session存储了cookie中
  - 默认过期31天



### 静态资源

- 配置
  - settings中添加STATICFILES_DIRS = [ path ]
  - 之后可直接使用
- 模板中使用
  - 先加载
  - {% load staticfiles %}
  - 再使用
  - {% static 'path' %}
- 只有在debug开启的情况下存在
- 关闭debug就不能使用静态资源了



### Bootstrap

- 可视化生成代码
- <http://www.bootcss.com/p/layoutit/>



### homework

- 文件上传，存储路径设计
- 缓存换成redis






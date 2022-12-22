本文叙述的是使用sqlalchemy的orm，来生成完整SQL语句，属于sqlalchemy的sql expression的使用，不属于常用的功能，如果有这个需求，可以在使用orm的情况下，更方便的生成和管理SQL语句，而不用手动处理字符串。

> orm => sql => logic

下面是数据库模型demo，无论使用的是什么框架，用何种方式来定义了model，不影响本文所使用的方法。

```python
class User(db.Model):
    __tablename__ = "dev_user"
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    username = db.Column(db.String(80), unique=True, doc="用户名", comment="用户id")
    email = db.Column(db.String(120), unique=True, doc="用户邮箱", comment="用户邮箱")
    is_active = db.Column(db.Boolean, default=False, doc="已激活", comment="是否已激活")
    phone = db.Column(db.String(20), index=True, doc="用户手机号", comment="用户手机号")
    age = db.Column(INTEGER(), doc="用户年龄", comment="用户年龄")

    def __repr__(self):
        return f"<User {self.username!r}>"


class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    content = db.Column(db.Text, comment="博客内容")
    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("dev_user.id"), index=True,
                        doc="用户id", comment="用户id")


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    comment = db.Column(db.String(150), doc="用户评论", comment="用户评论")
    user_id = db.Column(INTEGER(unsigned=True), index=True, doc"用户id", comment="用户id")


class UserInfo(db.Model):
    __tablename__ = "user_info"
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey("dev_user.id"),
												index=True, doc="用户id", comment="用户id",)
    user = db.relationship("User", backref="user_info", uselist=False)
    company = db.Column(db.String(100), unique=True, doc="公司简称", comment="公司简称")
```

精确查询
```python
query = select(User).where(User.username == 'Mike')
print(query.compile(compile_kwargs={'literal_binds': True}))
```

输出为：
```shell
SELECT dev_user.id, dev_user.username, dev_user.email, dev_user.is_active, dev_user.phone, dev_user.age 
FROM dev_user 
WHERE dev_user.username = 'Mike'
```

模糊查询

```python
query = Query(Blog).where(Blog.title.contains("sqlalchemy"))
# query = Query(Blog).filter_by(**{"title": "sqlalchemy"})
print(query.statement.compile(compile_kwargs={'literal_binds': True}))
```

输出为：

```shell
SELECT blog.id, blog.title, blog.content, blog.user_id 
FROM blog 
WHERE (blog.title LIKE '%' || 'sqlalchemy' || '%')
```

Query对象实际上是`Session.query()`方法的返回，可以发现Query对象的属性statement，其实就是select方法的返回值，sql语句对象。

单独构建Query对象，也可以使用session来执行

```python
query = Query(Blog).where(Blog.id == 1)
obj = query.with_session(session).one()
```

官方示例：

```python
from sqlalchemy.orm import Query

query = Query([MyClass]).filter(MyClass.id == 5)
result = query.with_session(my_session).one()
```

只查询单个字段：

```python
query = select(Blog).where(Blog.title.contains("sqlalchemy"))
print(query.with_only_columns(Blog.id).compile(compile_kwargs={'literal_binds': True}))
```

复杂一些的查询，使用Query和使用select方法来构建，大体相同

```python
query = Query([Blog, User]).join(User, Blog.user_id == User.id).where(Blog.title.contains("sqlalchemy"))
# query = Query(Blog).filter_by(**{"title": "sqlalchemy"})
print(query.statement.compile(compile_kwargs={'literal_binds': True}))
```

输出：
```shell
SELECT blog.id, blog.title, blog.content, blog.user_id, dev_user.id AS id_1, dev_user.username, dev_user.email, dev_user.is_active, dev_user.phone, dev_user.age 
FROM blog JOIN dev_user ON blog.user_id = dev_user.id 
WHERE (blog.title LIKE '%' || 'sqlalchemy' || '%')
```
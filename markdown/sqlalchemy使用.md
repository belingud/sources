# attention

使用`session.query`代替`model.query`，`model.query`需要数据库数据映射到模型，即时修改的数据库数据使用`model.query`可能不会直接查询出来

> `session.add()`执行之后，会将SQL语句添加到pending里面，再次使用`session.query`会强制执行pending中的SQL，然后再进行查询操作，而`model.query`不会强制执行pending中的SQL。(具体的原理和实现方式待研究。)

# session

首先创建一个db对象，这个对象有flask_sqlalchemy中关于数据库的所有封装

```python
from flask import Flask
from flask_sqlalchemy imort SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app, engine_options={'pool_recycle': 3600, 'pool_size': 20})
# session = db.session
```

Flask_sqlalchemy封装了很多SQLAlchemy的很多操作，可以直接使用flask中app的config来生成数据库连接，使用SQLlchemy原生方法来生成数据库连接可以使用，sqlalchemy默认的引擎是MySQLdb，`pip install mysql-python`，但是这个库已经不支持python3了，在python3环境下安装会出现`ModuleNotFoundError: No module named 'ConfigParser'`错误，因为python3将`ConfigParser.py`文件改成了`configparser.py`，将文件，也就是模块，复制一份为`ConfigParser.py`可以解决问题。

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
# 数据库+引擎://用户:密码@地址:端口/库?charset=utf8
mysql_uri = "mysql+pymysql://root:root@127.0.0.1:3306/SQLAlchemyTest?charset=utf8"

# paramstyle in ["qmark", "numeric", "named", "format" or "pyformat"]
engine = create_engine(
    mysql_uri,
    paramstyle=None,
    echo=True,
    echo_pool=True,
    pool_pre_ping=True,  # 悲观方式，每次执行语句先执行select语句实现ping的功能，可以在执行失败后重试
)
session_caller = sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True, info=None)
session = session_caller()
# session = scoped_session(session_factory=Session_caller, scopefunc=None)
```

`create_engine`接受的参数`paramstyle`是python默认的参数风格类型，在[PEP249(paramstyle)](https://www.python.org/dev/peps/pep-0249/#paramstyle)中有详细的讲解

> 一般使用pymysql来作为sqlalchemy的引擎，但是connectionless情况下在`paramstyle`上，踩到了sqlalchemy和pymysql的坑，pymysql在`__init__.py`指定了参数放个为`pyformat`，所以如果你想指定`paramstyle`这个参数，应该指定为`None`或者`pyformat`，否则会导致出错。
>
> 在connection模式下正常。
>
> 如果不涉及transaction，推荐使用connection模式。即通过`engine.connect()`创建连接，执行SQL

使用`named`

```python
# 使用named
engine = create_engine(mysql_uri, paramstyle='named')
session = sessionmaker(engine)()
sql = 'select * from dev_user where id={}'
session.execute(sql.format(':user_id'), {'user_id': 100}).fetchone()
# sqlalchemy 并没有将:user_id格式化，而是直接传给了pymysql，导致出错
# ProgrammingError: (pymysql.err.ProgrammingError) (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ':user_id' at line 1")
# [SQL: select * from dev_user where id=:user_id]
# [parameters: {'user_id': 100}]
```

使用`pyformat`

```python
# 使用pyformat
engine.paramstyle = 'pyformat'
session.execute(sql.format('%(user_id)s'), {'user_id': 100}).fetchone()
# sqlalchemy 没有获取到params参数
# ProgrammingError: (pymysql.err.ProgrammingError) (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '%(user_id)s' at line 1")
# [SQL: select * from dev_user where id=%%(user_id)s]

# 而使用named风格的参数则没问题
session.execute(sql.format(':user_id'), {'user_id': 100}).fetchone()
# SQL:
# select * from dev_user where id=%(user_id)s
# {'user_id': 101}
```

sqlalchemy有三种使用方式：

- raw sql
- sql expression
- ORM

前两种成为core方式，**注意**如果是sqlalchemy+cx_oracle的话, 需要禁掉 connection pool, 否则会有异常. 方法是设置sqlalchemy.poolclass为sqlalchemy.pool.NullPool

对于事务的支持

创建连接开启事务，对于添加而没有commit的数据可以创建保存点

```python
db.session.add(u1)
# 创建一个save point
db.session.begin_nested()

db.session.add(u2)
db.session.rollback()
# 只回退u2，不回退u1
db.session.commit()
```

下面是数据库模型demo

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



# 多数据库支持

flask_sqlalchemy使用bind的概念来绑定多个数据库

```python
# 在配置config类中可以使用
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/main'
    SQLALCHEMY_BINDS = {
    		'users':        'mysqldb://localhost/users',
    		'appmeta':      'sqlite:////path/to/appmeta.db'
		}
# 在app.config属性的设置中可以使用
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/main'
app.config["SQLALCHEMY_BINDS"] = {
    'users':        'mysqldb://localhost/users',
    'appmeta':      'sqlite:////path/to/appmeta.db'
}
```

在flask_sqlalchemy中，有很多封装有bind参数，可以在其中指定多数据库设置中的某一个，比如

```python
db.session.execute(sql, bind='user')
```

在SQL上的区别为：

```mysql
-- 不使用bind
SELECT user.username AS username_1 FROM user WHERE user.id = 100;
-- 使用bind
SELECT test.user.username AS username_1 FROM test.user WHERE test.user.id = 100;
-- 表名前缀为数据库名
```

在数据库的定义中使用多数据库支持

```python
class User(db.Model):
    __tablename__ = "user"
    # 指定`__bind_key__`在执行sql语句时会直接选择指定的数据库
    __bind_key__ = 'users'
    # 或者使用__table_args__
    __table_args__ = {
        'schema': "users",  # 指定bind
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }
    # __table_args__也可以使用元组
    # __table_args__ = (
    #	    db.UniqueConstraint("username", "id", name="uix_username_id"),
    #     db.Index("ix_username", "username")
    # )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    # sqlalchemy的多态特性
    __mapper_args__ = {
        "order_by": username.desc()
    }

# 或者使用创建对象方式创建表模型
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    info={'bind_key': 'users'}
)
```

# 基本使用（CRUD）

简单查询

1. 添加

利用db.session来添加数据

```python
user = User(username='Jack', email='jack@email.com')
db.session.add(user)
db.session.commit()  # 手动commit
user = User(username='Vic', email='vic@email.com')
info = UserInfo(user=user, company='Google')
# 添加多个对象
db.session.add_all([user, info])
db,session.commit()
```

2. 删除

Query对象的delete方法

update和delete方法接受一个可选参数`synchronize_session=evaluate`，`synchronize_session`可选三个值：

- `False`：更新数据库数据，不更新session中查询到的数据
- `fetch`：更新数据库数据，并重新从数据库读取数据
- `evaluate`：默认参数，如果出现session中的数据和数据库数据不一致，session无法判断如何处理，会抛出`InvalidRequestError`异常

```python
rows = db.session.query(User).filter(User.id == 101).delete(synchronize_session='evaluate')
```

但是，如果直接删除外键关联的数据，会报错，不过可以使用`session.delete()`方法，可以处理relationship的外键配置，如果配置了cascade='all,delete-orphan'，就会去删除从表的数据。

`session.delete(instance)`

```python
db.session.query(User).filter(User.id == 101).delete()
# IntegrityError: (pymysql.err.IntegrityError) (1451, 'Cannot delete or update a parent row: a foreign key constraint fails (`test`.`user_info`, CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `dev_user` (`id`))')

instance = db.session.query(User).filter(User.id == 101).scalar()
db.session.delete(instance)
# 删除成功返回1
```



3. 修改

修改有两种方式，修改属性然后提交，或者修改查询集的值

```python
# 修改对象属性
user = db.session.query(User).filter(User.id == 102).first()
user.username = 'Thomas'
db.session.add(user)
db.session.commit()
# 修改查询集Query的值
user_query = db.sessin.query(User.id < 100).update({'is_activate': 0})
db.session.commit()
```

4. 查询

**`filter_by`**

`filter_by`查询条件是`=`或者`and`的，单条件查询,条件必须关键字参数，而且and连接，返回一个query对象

```python
# scalar只返回一个，如果没有或者有多个返回会抛出MultipleResultsFound异常
db.session.query(User).filter_by(id=101).scalar()
# 多个模型数据查询，默认查询第一个模型User的id为101的数据
db.session.query(User, UserInfo).filter_by(id=101).all()
```

**`filter`**

`filter`接受的参数类型不同，可以多个过滤条件，返回的query对象

根据主键id可以直接用`get`进行查询

```python
db.session.query(User).get(100)
# 和Django一样，只获取一个结果，多个查询结果抛异常，没有则返回``None``
```

和Django的ORM不同，sqlalchemy把一些条件放到了model字段的属性中，比如`order_by`，和`as`

```python
from sqlalchemy import desc, asc
query.order_by(desc(User.owned))
db.session.query(User.id).filter().order_by(asc(User.id)).offset(10).limit(10).all()
# SQL:
#  SELECT dev_user.id AS dev_user_id
# FROM dev_user ORDER BY dev_user.id DESC
# LIMIT %(param_1)s, %(param_2)s
# {'param_1': 10, 'param_2': 10}
db.session.query(User.username.label('name')).filter()
# 将username起别名为name
# SQL:
# SELECT dev_user.username as name
# FROM dev_user
```

首先是一些从query中获取数据的方法，`all()`，`first()`，`one()`，`scalar()`，`get()`，`one_or_none()`

- all: 返回所有数据

- first: 所有rows里面取第一行，如果为没有结果则为None,不会抛异常

- one: 返回的rows必须是只有一行，有多行或者没有数据都会抛异常

- one_or_none： 返回的rows必须是一行或者没有数据，有多行数据就会抛异常

- scalar：返回的rows必须是一行或者没有数据，有多行数据就会抛异常，并且scalar只会取result里面的第一个结果集



**=，<，>的查询**

```python
# from sqlalchemy import true
db.session.query(User.id, User.username).filter(User.is_activate==db.true())

# 组合查询
db.session.query(User.username, UserInfo.company).filter(User.id==103, User.username=='Zachary Moreno').all()
# 组合查询也可以使用and_，翻译成的SQL相同
from sqlalchemy import and_, or_
db.session.query(User.username, UserInfo.company).filter(and_(User.id==103, User.username=='Zachary Moreno')).all()
# 翻译成的SQL：
# SELECT dev_user.username AS dev_user_username, user_info.company AS user_info_company
# FROM dev_user, user_info
# WHERE dev_user.id = %(id_1)s AND dev_user.username = %(username_1)s
# params: {'id_1': 103, 'username_1': 'Zachary Moreno'}

db.session.query(User).filter(User.id < 20).all()
db.session.query(User).filter(User.create_at > '2020-02-02 00:00:00')
```

**模糊查询**

```python
db.session.query(User.username).filter(User.email.startswith('123')).all()
db.session.query(User.username).filter(User.email.like('123%'))
# SELECT dev_user.username from dev_user where dev_user.email like '123%'
db.session.query(User.username).filter(User.email.endswith('123')).all()
```

**join**

join进行连表操作

```python
db.session.query(Comment.comment.label('user_comment'), User.id.label('user_id'), User.username.label('username')).join(User, User.id==Comment.user_id).filter(User.id<100).order_by(User.id.desc()).all()  # desc是字段的方法
# 对应SQL：
# SELECT comment.comment AS user_comment, dev_user.id AS user_id, dev_user.username AS username
# FROM comment INNER JOIN dev_user ON dev_user.id = comment.user_id
# WHERE dev_user.id = %(id_1)s
# params: {'id_1': 100}
```

可以利用sqlalchemy的别名进行多次join

```python
from sqlalchemy.orm import aliased
Comment_alias = aliased(Comment, name='comment_alias')
db.session.query(User.id, User.username, User.email, User.phone, Comment.comment).join(Comment, Comment.user_id == User.id).join(Comment_alias, Comment_alias.user_id == User.id).all()
# SQL:
# SELECT dev_user.id AS dev_user_id, dev_user.username AS dev_user_username, dev_user.email AS dev_user_email, dev_user.phone AS dev_user_phone, comment.comment 
# FROM dev_user INNER JOIN comment ON comment.user_id = dev_user.id INNER JOIN comment AS comment_alias ON comment_alias.user_id = dev_user.id
```



**offset/limit**

```python
from sqlalchemy import true

db.session.query(User.username, User.phone, User.email).filter(User.is_active == true()).order(User.age.desc()).offset(10).limit(20)
# SQL:
# SELECT dev_user.username AS dev_user_username, dev_user.phone AS dev_user_phone, dev_user.email AS dev_user_email
# FROM dev_user
# WHERE dev_user.is_active = true ORDER BY dev_user.age DESC
# LIMIT %(param_1)s, %(param_2)s
# {'param_1': 10, 'param_2': 20}

```

**in/not in/is null/is not null**

```python
# in
db.session.query(User).filter(User.id.in_([100, 103, 105]))
# not in
db.session.query(User).filter(~User.id.in_([100, 103, 105]))
# is null
from sqlalchemy import null
db.session.query(User).filter(User.email == null())
# is not null
db.session.query(User).filter(User.email != null())
```

**select_from**

指定从哪个数据表中获取数据，其实获取的字段可以在query中直接指定，`select_from`和`join`中的表不能相同

```python
db.session.query(User).select_from(Comment).join(User, Comment.user_id == User.id).all()
# 只获取User中的数据，即query中的model
# SELECT dev_user.id AS dev_user_id, dev_user.username AS dev_user_username, dev_user.email AS dev_user_email, dev_user.is_active AS dev_user_is_active, dev_user.phone AS dev_user_phone, dev_user.age AS dev_user_age
# FROM comment INNER JOIN dev_user ON dev_user.id = comment.user_id
```


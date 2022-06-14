存储过程的执行过程对外是不可见的，使用`select`可以进行对外输出，在控制台可见，使用代码执行存储过程时，如果有多个`select`语句，并且没有赋值给变量，会有多个输出，通常以数组形式返回。

因为存储过程中可能会执行很多语句，为了更好的控制事务，输出异常信息，可以使用`CONTINUE HANDLER`

在存储过程的开始定义变量 MSG 来存储异常信息，这是一个`CONTINUE HANDLER`，可以用来捕捉异常。

```sql
-- 开头
DECLARE V_COMMIT INT DEFAULT 2; -- 定义事务用，1为正常，-10为失败
DECLARE MSG TEXT; -- 异常信息
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1 MSG = MESSAGE_TEXT;
        SET V_COMMIT = -10;
    END;
START TRANSACTION;
```

执行完成中间的 SQL 语句，在存储过程的结尾处处理状态信息

```sql
-- 结束
IF V_COMMIT = -10 THEN
    ROLLBACK;
    SELECT MSG AS 'STATUS';
ELSE
    COMMIT;
    SELECT 'COMMIT' AS 'STATUS';
END IF;
```

完整的创建存储过程的语句：

```sql
DELIMITER $$
DROP PROCEDURE IF EXISTS proc_name;
CREATE PROCEDURE proc_name(IN _id int, OUT _result varchar(64))
BEGIN
    -- start
    DECLARE V_COMMIT INT DEFAULT 2; -- 定义事务用，1为正常，-10为失败
    DECLARE MSG TEXT; -- 异常信息
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        BEGIN
            GET DIAGNOSTICS CONDITION 1 MSG = MESSAGE_TEXT;
            SET V_COMMIT = -10;
        END;
    START TRANSACTION;

    -- 需要执行的SQL语句
    SELECT result INTO _result FROM demo WHERE id = _id;

    -- end
    IF V_COMMIT = -10 THEN
        ROLLBACK;
        SELECT MSG AS 'STATUS';
    ELSE
        COMMIT;
        SELECT 'COMMIT' AS 'STATUS';
    END IF;
END;
DELIMITER ;
```

在 Python 中调用存储过程，使用不同的连接库，内部有不同的封装，如果使用sqlalchemy+mysql-connector来连接数据库

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "mysql+mysqlconnector://root:123456@localhost:13306/demo?charset=utf8mb4",
)
Session = sessionmaker(bind=engine)
session = Session(bind=conn, expire_on_commit=False)
with session.begin():
    connection = session.bind.engine.raw_connection()
    with connection.cursor() as cursor:
        # result中保存了存储过程IN和OUT的参数
        result: tuple = cursor.callproc(
            'proc_name',  # 存储过程名
            [1, '@_what_ever']  # 存储过程参数
        )
        # mysqlconnector库来连接MySQL，用stored_result来获取存储过程中的输出
        for r in cursor.stored_results():
            status: list = r.fetchall()
            print(status)  # [('COMMIT',)]
```

如果使用pymysql来连接数据

```python
engine = create_engine(
    "mysql+pymysql://root:123456@localhost:13306/apmos?charset=utf8mb4",
    echo=True
)
Session = sessionmaker(bind=engine)
session = Session(bind=engine, expire_on_commit=False)
with session.begin():
    connection = session.bind.engine.raw_connection()
    with connection.cursor() as cursor:
        # res只保存了传入callproc方法的参数
        res: list = cursor.callproc(
            'test',  # 存储过程名
            [1, '@_what_ever']  # 存储过程参数
        )
        print(cursor.fetchall())  # (('COMMIT',))
        cursor.nextset()  # 使用nextset方法来获取下一个输出
        print(cursor.fetchall())  # ()
        # 需要使用select语句来获取存储过程的OUT输出
        # 格式为`@_<proc_name>_<index>`，index为传入存储过程参数的下标
        cursor.execute('select @_test_1')
        print(cursor.fetchall())
```

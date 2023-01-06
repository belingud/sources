本文以MySQL窗口函数`ROW_NUMBER`来作为示例，说明sqlalchemy如何使用窗口函数，ORM语句的一般写法，因为sqlalchemy非常复杂，也有其他写法，但是与本文的写法大体相同，只有细微差异。


这里定义一个使用场景，假如我们有一张表，用于记录多个平台虚拟货币的价格，每隔五分钟更新一次，以某一个以平台名和某个币种确定这个时间点的数据，但是因为网络IO的原因，入库的时间并不确定，同一批数据写入时间有差异，如果我们在查看数据时候，有一部分价格的数据还没有更新，那我们希望使用最近的一条数据。

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Numeric, DateTime
Base = declarative_base()


class SymbolPrice(Base):
    __tablename__ = "symbol_price"

    id = Column(INTEGER(unsigned=True), primary_key=True)
    platform = Column(String(16), comment="平台")
    symbol = Column(String(8), comment="币种")
    price = Column(Numeric, comment="价格")
    mark_time = Column(DateTime, comment="价格的对应时间")
```

这里的一种解决方式就是使用窗口函数，例如`ROW_NUMBER`，根据*平台名*加*币种*作为`PARTITION`，查询时间段内的数据，并且按照时间排序取最近的数据。

首先确定SQL需要怎么写，因为`PARTITION`只能使用单个字段，所以需要将数据进行预处理，使用`concat`连接平台和币种，作`PARTITION`的字段。

```sql
select *, concat(platform, symbol) as pc from symbol_price
where mark_time >= '2023-01-01 09:55:00' and mark_time < '2023-01-01 10:05:00'
```

然后使用`ROW_NUMBER`来查询最近的一条

```sql
select platform, symbol, price, mark_time from (
    select platform, symbol, price, mark_time,
    row_number() over(partition by c.pc order by c.mark_time desc) as row_num from (
        select *, concat(platform, symbol) as pc from symbol_price
        where mark_time >= '2023-01-01 09:55:00' and mark_time < '2023-01-01 10:05:00'
    ) c
) t where row_num = 1;
```

然后使用sqlalchemy来实现这个语句，使用sqlalchemy需要一个子查询一个子查询的实现

```python
from sqlalchemy import func, select

# concat子查询
stmt = select(
    SymbolPrice.platform,
    SymbolPrice.symbol,
    SymbolPrice.price,
    SymbolPrice.mark_time,
    func.concat(SymbolPrice.platform, SymbolPrice.symbol).label("pc"),
).where(
    SymbolPrice.mark_time >= datetime.datetime(2023, 1, 1, 9, 55),
    SymbolPrice.mark_time < datetime.datetime(2023, 1, 1, 10, 5),
).subquery()
# 计算行号子查询
row_sub = select(
    stmt.c.platform,
    stmt.c.symbol,
    stmt.c.price,
    stmt.c.mark_time,
    func.row_number().over(
        partition_by=stmt.c.pc, order_by=stmt.c.mark_time.desc()
    ).label("row_num"),
).subquery()

query = select(row_sub).where(row_sub.c.row_num == 1)
```

对于使用`session`对象，或者使用flask-sqlalchemy的`db.session`只需要将上面代码中的`select`改成`session`或者`db.session`，因为`session`或者`db.session`返回的是一个绑定数据库连接的`sqlalchemy.orm.Query`对象，在生成ORM语句上和`select`方法大体相同，不再赘述。

会得到下面的语句：

```python
str(query.compile(compile_kwargs={"literal_binds": True}))
"""
SELECT anon_1.platform, anon_1.symbol, anon_1.price, anon_1.mark_time, anon_1.row_num
FROM (SELECT anon_2.platform                                                           AS platform,
             anon_2.symbol                                                             AS symbol,
             anon_2.price                                                              AS price,
             anon_2.mark_time                                                          AS mark_time,
             ROW_NUMBER() OVER (PARTITION BY anon_2.pc ORDER BY anon_2.mark_time DESC) AS row_num
      FROM (SELECT symbol_price.platform                              AS platform,
                   symbol_price.symbol                                AS symbol,
                   symbol_price.price                                 AS price,
                   symbol_price.mark_time                             AS mark_time,
                   CONCAT(symbol_price.platform, symbol_price.symbol) AS pc
            FROM symbol_price
            WHERE symbol_price.mark_time >= '2023-01-01 09:55:00'
              AND symbol_price.mark_time < '2023-01-01 10:05:00') AS anon_2) AS anon_1
WHERE anon_1.row_num = 1
"""
```


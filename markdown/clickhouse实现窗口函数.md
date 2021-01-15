## 使用clickhouse的query语句，实现mysql中的ROW_NUMBER和RANK窗口函数

目标是实现一个语句查询到分数的排行和每个课程的分组的行号.

简单描述一下思路：

1. 首先对clickhouse数据进行初步的处理，初步的聚合或去重等，避免`select`出现字段不在group聚合中的错误
2. 将干净的数据按照课程聚合出数据对应的数组数据
3. 取出数组和需要的id等数据

首先是第一步：

```sql
-- 这里通过unique_id进行去重，clickhouse数据是增量的，没有对原始数据进行update，所以使用unique_id保持一次学习数据的一致性
select *
from score_record
where lesson_id in (1, 2)
  and score > 0
order by score desc
limit 1 by unique_id;
```

第二步：

```sql
select lesson_id,
       groupArray(score)              as array_val,
       arrayEnumerate(array_val)      as row_num,
       arrayEnumerateDense(array_val) as rank
from (select *
      from score_record
      where lesson_id in (1, 2)
        and score > 0
      order by score desc
      limit 1 by unique_id) tmp
group by lesson_id;
```


```sql
select *
from (select score, row_num, rank, lesson_id
      from (select lesson_id,
                   groupArray(score)              as array_val,
                   arrayEnumerate(array_val)      as row_num,
                   arrayEnumerateDense(array_val) as rank
            from (select *
                  from score_record
                  where lesson_id in (1, 2)
                    and score > 0
                  order by score desc
                  limit 1 by unique_id) tmp
            group by lesson_id) g array join
           array_val as score, row_num, rank
      order by lesson_id, row_num)
where row_num < 10;
```
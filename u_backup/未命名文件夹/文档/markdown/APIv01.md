## 标题结构

排行榜标题的框架，包含二级的中职高职，三级的院校热度，四级的行业分类

- 接口地址：/title/
  - 示例`http://192.168.110.162:8000/billboard/title/`
- 请求方式：GET
- 输入参数：
  - None
- code
  - 正确参数
    - 200
  - 错误参数
    - 404
- 返回参数
  - code
  - msg
  - data
    - top
    - news
- 返回json示例

```json
/* 成功示例 */
{
    "code": 200,
    "msg": "ok",
    "data": [
        {
            "name": "中职榜",
            "info": [
                {
                    "keyword": "院校热度",
                    "id": 1
                },
                {
                    "keyword": "专业热度",
                    "id": 2
                },
                {
                    "keyword": "垂直行业榜",
                    "values": [
                        {
                            "keyword": "汽车",
                            "id": 3
                        },
                        {
                            "keyword": "航",
                            "id": 4
                        }]}]},
        {
            "name": "高职榜",
            "info": [
                {
                    "keyword": "院校热度",
                    "id": 6
                },
                {
                    "keyword": "专业热度",
                    "id": 7
                },
                {
                    "keyword": "垂直行业榜",
                    "values": [
                        {
                            "keyword": "医疗",
                            "id": 8
                        },
                        {
                            "keyword": "旅游",
                            "id": 9
                        }]}]},
        {
            "name": "热招榜",
            "info": [
                {
                    "city": "北京",
                    "id": 11
                },
                {
                    "city": "上海",
                    "id": 12
                },
                {
                    "city": "广州",
                    "id": 13
                },
                {
                    "city": "深圳",
                    "id": 14
                }]}]}
```



```json
/* 错误示例 */
{
    "code": 404,
    "msg": Exception,
    "data": ""
    }
}
```



## 新闻列表

点击首页的新闻类型，进入某个类型的新闻列表

- 接口地址
  - /news/news_list/
  - 示例
    - `http://192.168.110.162:8000/news/news_list/1/`:1为news_type_id
    - `http://192.168.110.162:8000/news/news_list/1/?page=3`
- 请求方式
  - GET
- 传入参数
  - news_type_id
  - page
- code
  - 正确参数
    - 200
  - 错误参数
    - 404
- 返回参数
  - code
  - msg
  - data
    - list
- 返回json示例

```json
//成功示例
{
    "code": 200,
    "msg": "ok",
    "data": [
        {"title": title, "pub_time": time, "id": id},
        {"title": title, "pub_time": time, "id": id},
        {"title": title, "pub_time": time, "id": id}
    ]    
}
```



## 新闻详情

新闻的内容接口，点击链接阅读新闻

- 接口地址
  - /news/info/
  - 示例
    - `http://192.168.110.162:8000/news/info/1/`：1为news_id
- 请求方式
  - GET
- 参数
  - news_id
- code
  - 正确参数
    - 200
  - 错误参数
    - 404
- 返回参数
  - code
  - msg
  - data
    - title
    - time
    - content
- 返回json示例

```json
//成功示例
{
    "code": 200,
    "msg": "ok",
    "data":{
        "id": id, 
        "title": string,
        "author": string,
        "tags": taglist,
        "source": string,
        "pub_time": time,
        "content": content
    }
}
```



```json
//错误示例
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 6,
            "name": "电路工程师/技术员",
            "score": 49,
            "job_ranking_type": 1
        },
        {
            "id": 1,
            "name": "工艺/制造工程师",
            "score": 125,
            "job_ranking_type": 1
        }
    ]
}
```



## 排行榜API

排行榜的综合接口，能够通过结构目录里面的id进行请求，返回从大到小排序的一个列表

- 接口地址
  - `billboard/ranking/<ranking_type_id>/`
  - 示例
    - `http://192.168.110.162:8000/billboard/ranking/1/`：1代表中职-学校的id，即url中的ranking_type_id
    - `http://192.168.110.162:8000/billboard/ranking/4/?page=3`
- 请求方式：GET
- 参数：
  - ranking_type_id
  - page
- code
  - 正确参数
    - 200
  - 错误参数
    - 404
- 返回参数
  - code
  - msg
  - data
- 返回json示例

```json
//成功示例
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5197,
            "score": 644,
            "college_ranking_type": 12,
            "college": {
                "id": 74,
                "name": "三亚航空旅游职业学院"
            }
        },
        {
            "id": 5199,
            "score": 221,
            "college_ranking_type": 12,
            "college": {
                "id": 5251,
                "name": "兰州航空工业职工大学"
            }
        },
        {
            "id": 5198,
            "score": 130,
            "college_ranking_type": 12,
            "college": {
                "id": 3460,
                "name": "信阳航空服务学校"}}]}
```



## 推荐页面

随机推荐文章

- 接口
  - `news/recommend/`

- 请求方式
  - GET
- 参数：空
- code
  - 200
  - 404
- 返回json示例

```json
{
    "code": 200,
    "msg": "ok",
    "data": [
        {
            "id": 26,
            "title": "志合越山海 ——有色金属行业与职业教育协同“走出去”赴赞比亚办学记",
            "pub_time": "2019-08-17"
        },
        {
            "id": 7,
            "title": "让职业教育再创辉煌",
            "pub_time": "2019-09-04"
        },
        {
            "id": 32,
            "title": "重庆出台职业教育改革实施方案 这6所院校首批试点转型为应用技术型大学",
            "pub_time": "2019-07-04"
        },
        {
            "id": 15,
            "title": "金华开发区园区企业数字化转型激发制造业新活力",
            "pub_time": "2019-09-04"
        },
        {
            "id": 12,
            "title": "2019中国制造业企业500强创新成效显著",
            "pub_time": "2019-09-04"
        }
    ]
}
```


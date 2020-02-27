# Scrapy

## Getting start

```bash
# create a new project named tutorial
scrapy startproject tutorial
# get in the root direction of your project
cd tutorial
# create a custom spider
scrapy genspider quotes quotes.toscrape.com
# scrapy genspider custom spider-name target domain

```



## Structure

```bash
├── scrapy.cfg 整个项目的配置文件，一个项目只有一个，存放在根目录下
└── tutorial  项目的Python文件所在的包
    ├── __init__.py
    ├── items.py  Item对象定义
    ├── middlewares.py  中间件
    ├── pipelines.py  存储item对象的逻辑
    ├── settings.py  配置爬虫的逻辑
    └── spiders  通过genspider命令生成的spider文件存放在这里
        ├── __init__.py
        └── quotes.py  spider文件，名字和我们genspider命令里指定的一样

注意：我们所有执行的命令都是在项目根目录下去执行
```



### Start spider

```bash
# scrapy crawl CustomSpiderName
scrapy crawl quotes
```



## robots.txt

定义了爬虫的规则，通常放在网站的根目录下。

```shell
Disallow:  /product/ 不允许爬取/product下的所有页面
allow:  /product/ 允许爬取
```



## Scrapy shell


```bash
# 后面的URL可以传也可以不传
scrapy shell 'http://quotes.toscrape.com/page/1/'
```

进入控制台以后，以下变量默认帮我们设置好了，无需要再import 或者初始化：

[s]   scrapy    scrapy模块
[s]   crawler    Crawler对象
[s]   item       爬取指定页面取获取的item对象，如果你传了url并且parse函数有返回item对象
[s]   request    url的Request对象
[s]   response   请求该url所返回的Response对象
[s]   settings   Settings对象，保存了我们项目所有的配置，包括settings.py里面所设置的内容。用来检测我们的配置是否生效
[s]   spider     Spider类的对象
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True])    抓取给定的url参数，并更新本地的request和response对象，默认跟随重定向跳转。
[s]   fetch(req)                 抓取一个Request对象，并更新局部变量（request/response/item）
[s]   shelp()          显示shell内的帮助，显示所有内置变量
[s]   view(response)    在浏览器中查看response结果



## DownloaderMiddleware



process_xxx函数的返回值：

| 函数              | 返回值    | 行为                                                         |
| ----------------- | --------- | ------------------------------------------------------------ |
| process_request   | None      | normal                                                       |
|                   | Response  | 停止后面的中间件process_request函数调用，<br>并直接返回Response对象给中间件链的process_response函数 |
|                   | Request   | 停止中间件链的调用，<br>安排该Request对象重新下载            |
|                   | Exception | 调用process_exception函数                                    |
| process_response  | Response  | normal                                                       |
|                   | Request   | 停止中间件链的调用，<br>安排该Request对象重新下载            |
|                   | Exception | 调用process_exception函数                                    |
| process_exception | None      | normal                                                       |
|                   | Response  | 停止后面的中间件process_exception函数调用，<br/>并直接返回Response对象给中间件链的process_response函数 |
|                   | Request   | 停止中间件链的调用，<br>安排该Request对象重新下载            |





### SpiderMiddleware

一般用于处理request，记录爬取的内容

监控redis

```shell
# 进入redis
redis-cli
# 监控redis
monitor
```

清除redis所有数据

```shell
flushdb
```




# AntConcept

## 状态码

### 2*

- 200    ok  请求成功，一般用于GET，POST请求
- 201    created    已创建
- 202    accepted    已接受
- 203    非授权信息。请求成功，但是meta信息不再原始服务器

### 3*

- 301    Moved Permanently    永久移动
- 302    Found    临时移动
- 303    SeeOther    查看其他地址，和301类似，GET重定向
- 304    NotModified    未修改，使用缓存

### 4*

- 400    BadRequest    客户端错误，请求无法理解
- 401    Unanthorized    未授权，要求身份认证
- 403    Forbidden    服务器理解客户端请求，但是拒绝执行此请求
- 404    NotFound    服务器无法根据客户端的请求找到资源
- 405    Method Not Allowed    请求方法被拒绝

### 5*

- 500    Not Implemented    服务器内部错误无法完成请求
- 502    Bad Gateway    网关错误
- 503    Service Unavailable    服务器不可用
- 504    Gateway Timeout    服务器超时

## request

请求头信息，是一个文本信息，可以缺失任何字段

- HTTP/1.1 200 OK
  - HTTP协议版本，状态码
- Connection: Keep-Alive
  - 连接状态，keepalive表示长连接
- Content-Encoding: gzip
  - 文本传输编码格式，gzip是一种网络压缩格式
- Date: Thu, 11 Aug 2016 15:23:13 GMT
  - 日期
- Kepp-Alive: timeout=5, max=1000
  - 超时时间5秒，最长时间1000秒
- Last-Modified: Mon, 25 Jul 2016 04:32:39 GMT
  - 上次确认时间
- Server: Apache
  - 服务器代理软件



## 爬虫逻辑

### 确定url

1. 全局刷新

对于全局刷新，需要观察地址栏的变化，例如页面的跳转、下一页的切换、局部数据在不同url中的展示，从地址栏拿到所需要的url



2. 局部刷新

对于有些页面的局部数据切换，例如在懒加载、局部刷新下一页，详情切换等情况，需要查看发出请求的ajax。打开浏览器的检查，在`network`里面查看`XHR`，是ajax请求发出的列表，在请求头里面可以查看url。

![](https://github.com/belingud/image/blob/master/typolra/XHRHeaders.png?raw=true)



确认需要爬取内容的url是爬虫启动的第一步。

### 如何解析数据

针对网站的结构，返回的数据类型，加载类型，可以确定我们爬取内容所需要使用的工具。



主要分析的是B/S模型中的数据抓取，服务器端一般返回的是HTML或json数据。对于HTML，可以拿到HTML源码，进行bs4、xpath、CSS选择，抓取相应的内容，对于json数据，python可以直接对其进行处理。



有些响应返回的xml数据，不同与HTML，xml数据需要进行不能通过CSS选择，但是可以通过xpath和bs4来进行处理。



他们都可以使用正则表达式来进行匹配相应的内容，匹配速度更快，但是正则表达式难以书写，和阅读，不建议使用。



### 获取数据

确认我们所需要的工具之后，需要进行测试，确认网站的反爬策略，一般的反扒策略分为几种：

- UserAgent
- cookie
- refer
- 自定义键值对(time等)

有一些其他的应对恶意访问的策略，比如：

- 动态加载：局部 src ---> src2，大致为将标签的src替换为脏数据，标签内隐藏一个真实数据的src，爬虫在抓取标签的src时，拿到的就是脏数据，一定程度上防御了恶意访问
- 验证码：用户登录系统的验证码，可以通过企业验证码解决方案
- 用户习惯：有些网站的反扒策略较为智能，通过分析访问者的动作来判断是否是正常用户，如果访问过于频繁，间歇过于短暂，会被限制访问。可以模拟用户的访问动作，限制爬虫程序的访问次数和间隔。

### 存储数据

拿到我们想要的数据之后，就可以考虑数据的存储方式问题，设计数据的格式，存储位置等，一般会被存储在txt、excel、csv中。



# wget



**wget命令**用来从指定的URL下载文件。wget非常稳定，它在带宽很窄的情况下和不稳定网络中有很强的适应性



- A<后缀名>：指定要下载文件的后缀名，多个后缀名之间使用逗号进行分隔；
- b：进行后台的方式运行wget；
- B<连接地址>：设置参考的连接地址的基地地址；
- c：继续执行上次终端的任务；
- C<标志>：设置服务器数据块功能标志on为激活，off为关闭，默认值为on；
- d：调试模式运行指令；
- D<域名列表>：设置顺着的域名列表，域名之间用“，”分隔；
- e<指令>：作为文件“.wgetrc”中的一部分执行指定的指令；
- h：显示指令帮助信息；
- i<文件>：从指定文件获取要下载的URL地址；
- l<目录列表>：设置顺着的目录列表，多个目录用“，”分隔；
- L：仅顺着关联的连接；
- r：递归下载方式；



# curl

根据参数可以实现非常多的网络请求方式

| 参数 | 说明                                               | 示例                                                         |
| ---- | -------------------------------------------------- | ------------------------------------------------------------ |
| -I   | 只显示头信息                                       |                                                              |
| -X   | 指定请求的方向                                     | 以PUT方法请求URL<br />curl -X PUT http://httpbin.org/put     |
| -v   | 显示连接的详细过程信息<br />包括请求头和响应头信息 | curl -vX https://cn.bing.com                                 |
| -A   | 伪装User-Agent信息                                 | curl -A Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A http://httpbin.org |
| -H   | 设置请求头信息                                     | curl -H "DNT:1" http://httpbin.org/headers                   |
| -o   | 下载资源并保存到指定的文件                         | curl -o baidu.jpg https://cambrian-images.cdn.bcebos.com/36773218021e19f7c5382481dd484853_1529466440372.jpeg |
| -d   | 设置Post请求参数                                   | curl -X POST -d "a=1&b=2" http://httpbin.org/post            |



# BS4

官方吹：



> Beautiful Soup提供一些简单的、python式的函数用来处理导航、搜索、修改分析树等功能。它是一个工具箱，通过解析文档为用户提供需要抓取的数据，因为简单，所以不需要多少代码就可以写出一个完整的应用程序。
>
>
>
> Beautiful Soup自动将输入文档转换为Unicode编码，输出文档转换为utf-8编码。你不需要考虑编码方式，除非文档没有指定一个编码方式，这时，Beautiful Soup就不能自动识别编码方式了。然后，你仅仅需要说明一下原始编码方式就可以了。



beautifulsoup通过由根节点寻找子节点的方式，来分析网页内容。



首先需要实例化一个BeautifulSoup()对象，将html传入到这个对象里面，会自动创建树形结构。



```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc)
print(soup.prettify())

#几个简单的浏览结构化数据的方法:
soup.title
# <title>The Dormouse's story</title>

soup.title.name
# u'title'

soup.title.string
# u'The Dormouse's story'

soup.title.parent.name
# u'head'

soup.p
# <p class="title"><b>The Dormouse's story</b></p>

soup.p['class']
# u'title'

soup.a
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

soup.find_all('a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find(id="link3")
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

# 从文档中找到所有<a>标签的链接:
for link in soup.find_all('a'):
    print(link.get('href'))

# 从文档中获取所有文字内容:
print(soup.get_text())

# 使用lxml作为解析器
soup_lxml = BeautifulSoup(html_doc, 'lxml')
print(soup_lxml.title)
```



# lxml

 lxml是python的一个解析库，支持HTML和XML的解析，支持XPath解析方式，而且解析效率非常高



XPath，全称XML Path Language，即XML路径语言，它是一门在XML文档中查找信息的语言，它最初是用来搜寻XML文档的，但是它同样适用于HTML文档的搜索



XPath的选择功能十分强大，它提供了非常简明的路径选择表达式，另外，它还提供了超过100个内建函数，用于字符串、数值、时间的匹配以及节点、序列的处理等，几乎所有我们想要定位的节点，都可以用XPath来选择



**通过xpath查找到的结果是一个列表**



```python
from lxml import etree
selector = etree.HTML(html_doc)
e = selector.cssselect('p.title')[0]  # list type
e.getchildren()[0].text  # list type
selector.findall('p')  # empty list
selector.findall('body')  # only get first level children
```



## Xpath

### 概念

- 节点
  - 元素，比如a标签、body/title等标签
  - 属性，标签的属性，比如class，src, href
  - 文本，在标签以内的内容
  - 命名空间
  - 处理指令、内置函数
  - 文档根节点，以/来表示
- 节点之间的关系
  - 父  ../
  - 子  ，body/div表示body下面的子节点div
  - 同胞   span/following-sibling::span 表示span相邻的一个span节点
  - 先辈/后代， body//a 表示body是a的先辈节点，a是body的后代节点。通常//开头，表示从根节点查找它的所有后代节点。
  - ./ 表示以当前节点为根节点，查找它的子节点
  - .// 表示以当前节点为根节点，查找它的后代节点
  - @href表示获取当前节点的href属性

```python
s = etree.HTML(html_doc)
s.xpath('//bookstore')
s.xpath('//bookstore//title/@larg')
s.xpath('//bookstore//title/text()')
s.xpath('//bookstore/nook[1]')  # count from 1
s.xpath('//bookstore/book[last()]')  # get the last element
s.xpath('//bookstore/book/title[@lang="en"]')
s.xpath('//a/@href')  # pick up all the link
# calculate in xpath
s.xpath('//book[price>29]')
```



使用xpath查找子节点，父节点，后代，先辈，以及内容属性



```python
r = requests.get('http://www.hao123.com')
# create selector to contor content of the html request before
selector = etree.HTML(r.text)

# 查找monkey="mingzhan-zfsitebar"的div的子节点a标签的href属性值
dom.xpath('//div[@monkey="mingzhan-zfsitebar"]/a/@href')

# 取出所有的a节点
for a in dom.xpath('//div[@monkey="mingzhan-zfsitebar"]/a'):
    print(a.xpath('./text()')[0], a.xpath('./@href')[0])
    
# 取第一个链接
dom.xpath('//div[@monkey="mingzhan-zfsitebar"]/a[1]/@href')
# 取最后一个链接
dom.xpath('//div[@monkey="mingzhan-zfsitebar"]/a[last()]/@href')
# 取前3个链接
dom.xpath('//div[@monkey="mingzhan-zfsitebar"]/a[position()<4]/@href')
```



Chrome浏览器xpath helper插件：https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl



CSS选择器插件：https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb




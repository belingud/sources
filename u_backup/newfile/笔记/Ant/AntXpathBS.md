## Download Pic



```shell
# download all the picture from xiachufang
curl https://xiachufang.com/|grep -oE 'https?://.+?\.(jpg,png)' xiachufang.html| cut -d '?' -f1|cut -d "@" -f1|xargs -i curl -O {}`

# curl 大写`-O`表示自动命名
# 在命令行里面写python代码

|python -c "python_code"
```





### 下载bilibili视频

```shell
curl -s 'https://api.bilibili.com/x/space/channel/video?mid=146668655&cid=27588&pn=1&ps=30&order=0&jsonp=jsonp&callback=__jp5' -H 'Referer: https://space.bilibili.com/146668655/channel/detail?cid=27588' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36' -H 'DNT: 1' --compressed| grep -oE '\{.+\}'|python -c "import json,sys; res = json.load(sys.stdin); [print('https://www.bilibili.com/video/av%s' % i['aid'] for i in res['data']['list']['archives'])]"|xaargs you-get {}
```



## BeautifulSoup

```python
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""


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



## lxml

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














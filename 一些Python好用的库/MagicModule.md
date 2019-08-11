## 文件读写

### excel读写：

1. xlwing：可读写加密excel文件，包含excel的新建、打开、修改、保存，支持Windows、Mac，Excel、WPS都能用。最强大的excel文件操作库

- xlwings能够非常方便的读写Excel文件中的数据，并且能够进行单元格格式的修改
- 可以和matplotlib以及pandas无缝连接
- 可以调用Excel文件中VBA写好的程序，也可以让VBA调用用Python写的程序。
- 开源免费，一直在更新

![](http://img.lte.ink/20190811181338.png)

官方网站：https://www.xlwings.org/

github地址：https://github.com/xlwings/xlwings

2. xlrd、xlwt、xlutils

xlrd是读excel，xlwt是写excel的库、xlutils － 操作 Excel 文件的实用工具，如复制、分割、筛选等。只能操作xls文件

注意单元格的跨度

github地址：

- xlrd：https://github.com/python-excel/xlrd
- xlwt：https://github.com/python-excel/xlwt
- xlutils：https://github.com/python-excel/xlutils

参考文章：https://www.cnblogs.com/jiangzhaowei/p/5856604.html

### word文件读写

.docx后缀的文件可以使用python-docx库来读写，是一个跨平台的库，.doc后缀的文件可以使用pypiwin32，这个库处理word文档的思路可以理解为：先创建一个word的application，用这个程序来新建、读取word等操作。但是这个库只能在Windows上使用，如果在Linux上操作.doc文件，建议先转成.docx格式的文件。可以使用pypiwin32来批量转格式。

```shell
pip install pypiwin32
```

示例：

```python
from win32com.client import Dispatch


app = Dispatch('Word.Application')
# 新建word文档
doc = app.Documents.Add()
# 运行下句代码后，s获得新建文档的光标焦点
s = app.Selection
# 用“Hello, World!“替换s代表的范围的文本
s.Text = 'Hello, world!'
# 使用Start，End指定字符范围
s.Start = 0
s.End = n
# s从第0个字符（第1个字符前的插入点）到第n个字符。
# 汉字是每字为1字符

# 相当于按下Delete键
s.Delete() 
# 相当于按下Ctrl+A
s.WholeStory() 
# 向左移动
s.MoveLeft()
# 向右移动2个字符，第1个参数是移动单位WdUnits，见下图
s.MoveRight(1, 2)
```

使用pypiwin32来批量转格式：

```python
from win32com import client as wc


# 创建word应用
word = wc.Dispatch("Word.Application")
doc = word.Documents.Open('path.doc')
doc.SaveAs('path.docx', 12)  # 12为docx
doc.Close()
# 退出应用
word.Quit()
```

然后在使用python-docx库来读写.docx后缀的文件，注意导入的模块名为docx

```python
import docx
```

github地址：

python-docx：https://github.com/python-openxml/python-docx

pypi地址：

pypiwin32：https://pypi.org/project/pypiwin32/

### mat文件读写

scipy

```python
import scipy.io
data = scipy.io.loadmat('data.mat')
matrix1 = data['matrix1'] 
matrix2 = data['matrix2']
scipy.io.savemat('data2.mat',{'matrix1':matrix1, 'matrix2':matrix2})
```

## 爬虫相关

### 文章抓取

1. python-goose： Goose 用于文章提取器

```shell
>>> from goose import Goose
>>> from goose.text import StopWordsChinese
>>> url  = 'http://www.bbc.co.uk/zhongwen/simp/chinese_news/2012/12/121210_hongkong_politics.shtml'
>>> g = Goose({'stopwords_class': StopWordsChinese})
>>> article = g.extract(url=url)
>>> print article.cleaned_text[:150]
```

github地址：https://github.com/grangier/python-goose

2. awesome-python-login-model

模拟登录一些知名的网站，为了方便爬取需要登录的网站，没有处理验证码

github地址：https://github.com/CriseLYJ/awesome-python-login-model

3. fake-useragent

伪装浏览器身份

```python
from fake_useragent import UserAgent
ua = UserAgent()
ua.chrome
# Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
```

4. newspaper

强大的提取 Web 的内容、文章的库，支持多种语言

github地址：https://github.com/codelucas/newspaper



## flask相关

### admin管理系统

1. flask-admin

一个微型管理系统，页面已经写好，稍微配置就可以运行

github地址：https://github.com/flask-admin/flask-admin

2. flask-adminlte-scaffold

flask-adminlte-handler是一个Python环境下的WEB后台管理系统脚手架，目标是用极少量的代码，快速构建小型WEB应用。请勿在大中型项目中进行尝试。

github地址：https://github.com/xiiiblue/flask-adminlte-scaffold

### 论坛框架

flaskbb

基于 Flask 框架做的论坛，功能有限，轻量级的论坛应用

github地址：https://github.com/flaskbb/flaskbb

### 限流

flask-limiter：一个 Flask 的扩展库，它可以根据访问者的 IP 限制其访问频率、次数等。用装饰器来实现功能

github地址：https://github.com/alisaifee/flask-limiter





## Tornado

### 社区项目

Young：基于 Tornado 框架、MongoDB 数据库，写的功能丰富的社区项目

github地址：https://github.com/shiyanhui/Young

## 服务器工具

**ngxtop**：解析 nginx 访问日志并格式化输出有用的信息，可以用来实时了解你的服务器正在发生的情况

github地址：https://github.com/lebinh/ngxtop

## 其他

**textfilter**：基于某 1w 词敏感词库，用 Python 实现几种不同的过滤方式

```python
from filter import DFAFilter

gfw = DFAFilter()
gfw.parse("keywords")
print "待过滤：售假人民币 我操操操"
print "过滤后：", gfw.filter("售假人民币 我操操操", "*")
```

github地址：https://github.com/observerss/textfilter

**mycli**：mycli 是一个带语法高亮、自动补全的 MySQL 命令行客户端工具。例如，连接数据库方法：`mycli -h localhost `

github地址：https://github.com/dbcli/mycli

**faker**：用于生成假数据的库

```python
from faker import Faker
fake = Faker()

fake.name()
# 'Lucy Cechtelar'

fake.address()
# '426 Jordy Lodge
#  Cartwrightshire, SC 88120-6700'

fake.text()
```

github地址：https://github.com/joke2k/faker

**records**：，Records 是一个支持大多数主流关系数据库的原生 SQL 查询第三方库。API 友好，使用简单、支持命令行模式、功能多样

```python
import records

db = records.Database('postgres://...')
rows = db.query('select * from active_users')    # or db.query_file('sqls/active-users.sql')
```

能够将数据库内容输出为不同的格式，比如json、YAML、xls、DataFrame、csv、dataset

github地址：https://github.com/kennethreitz/records

**tenacity**：使用该库可以优雅地实现各种需求的重试

```python
from tenacity import retry, stop_after_attempt

# 通过装饰器，实现遇到异常重试3次
@retry(stop=stop_after_attempt(3)) 
def get_data(url):
    response = requests.get(url)
    response_json = response.json()
```

github地址：https://github.com/jd/tenacity

**loguru**：一个让 Python 记录日志变得简单的库

```python
from loguru import logger
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
@logger.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)
```

github地址：https://github.com/Delgan/loguru
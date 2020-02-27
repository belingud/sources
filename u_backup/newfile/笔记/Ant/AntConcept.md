# 状态码

## 2*

- 200    ok  请求成功，一般用于GET，POST请求
- 201    created    已创建
- 202    accepted    已接受
- 203    非授权信息。请求成功，但是meta信息不再原始服务器

## 3*

- 301    Moved Permanently    永久移动
- 302    Found    临时移动
- 303    SeeOther    查看其他地址，和301类似，GET重定向
- 304    NotModified    未修改，使用缓存

## 4*

- 400    BadRequest    客户端错误，请求无法理解
- 401    Unanthorized    未授权，要求身份认证
- 403    Forbidden    服务器理解客户端请求，但是拒绝执行此请求
- 404    NotFound    服务器无法根据客户端的请求找到资源
- 405    Method Not Allowed    请求方法被拒绝

## 5*

- 500    Not Implemented    服务器内部错误无法完成请求
- 502    Bad Gateway    网关错误
- 503    Service Unavailable    服务器不可用
- 504    Gateway Timeout    服务器超时

# request

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

# Practice



1. 使用curl 去模拟请求httpbin.org网站
   - 无参patch
     - 发送一个patch请求     `curl -X PATCH "http://httpbin.org/patch" -H "accept: application/json"`
   - Auth
     - 基本验证账号密码    `curl -X GET "http://httpbin.org/basic-auth/vic/qwe" -H "accept: acception/json" `
   - status
     - url中加入状态码201    `curl -X POST "http://httpbin.org/status/201" -H "accept: text/plain"`
   - Request inspection
     - 获取请求状态IP    `curl -X GET "http://httpbin.org/ip"`
     - response: `{
         "origin": "114.242.26.65, 114.242.26.65"
       }`
   - Response inspection
     - 设置缓存时间    `curl -X GET "http://httpbin.org/cache/3000" -H "accept: application/json"`
   - Response formats
     - 请求一个html的返回     `curl -X GET "http://httpbin.org/html" -H "accept: text/html"`
   - Dynamic data
     - 请求一个uuid4的json    `curl -X GET "http://httpbin.org/uuid" -H "accept: application/json"`
   - Cookies
     - 设置Cookie    `curl -X GET "http://httpbin.org/cookies/set/vic/uuid4" -H "accept: text/plain"`
   - Image
     - 获取一张jpeg格式的图片    `curl -X GET "http://httpbin.org/image/jpeg" -H "accept: image/jpeg"`
   - Redirects
     - 临时重定向至Bing    `curl -X GET "http://httpbin.org/redirect-to?url=https%3A%2F%2Fcn.bing.com&status_code=302" -H "accept: text/html"`
   - Anything
     - 获取全部请求头    `http://httpbin.org/anything`
2. 使用wget去整站下载一个网站
   - `wget -a 3 -r -l 4 -p -k http:xiachufang.com`
   - -a  wait请求间隔时间
   - -r  地柜下载，下载链接的层数
   - -p  下载组成网页的图片等
   - -k  下载完成后，将绝对链接转变成相对链接，实现本地访问

3. 使用requests库模拟请求，实现大小写不敏感字典
   - practice_requests.py
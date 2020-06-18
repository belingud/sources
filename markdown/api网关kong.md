客户端访问上游API服务，通常由Kong的认证插件及其配置参数来控制。

kong的github项目地址: https://github.com/Kong/kong

使用kong之后，API请求将由kong接管转发。

![](https://camo.githubusercontent.com/d4d0dcb22c223db0bf2e301aab0dddb3015f1729/68747470733a2f2f6b6f6e6768712e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031382f30352f6b6f6e672d62656e65666974732d6769746875622d726561646d652e706e67)

# 安装

Kong是一个在Nginx运行的Lua应用程序，由lua-nginx-module实现。Kong和OpenResty一起打包发行，其中已经包含了lua-nginx-module。OpenResty不是Nginx的分支，而是一组扩展其功能的模块。

kong可以在多种操作系统环境下安装，比较方便的是使用docker进行安装

```shell
docker pull kong
```

需要注意的是kong依赖于`Postgres`或者`Cassandra`来存储认证信息，这里选择使用`Postgres`利用`docker-compose`来搭建kong的运行环境。

> docker desktop版本中默认集成了`docker-compose`，如果是Linux环境，需要使用`pypi`，或者直接下载可执行文件来安装`docker-compose`。`pip install docker-compose`

下面是`docker-compose.yml`文明的示例

```yaml
version: '3'
services:
  kong-database:
    image: postgres
    container_name: kong-database
    ports:
      - 5432:5432
    environment:
      - POSTGRES_USER=kong
      - POSTGRES_DB=kong
      - POSTGRES_PASSWORD=kong
    networks:
      - kong-net
    volumes:
      - "db-data-kong-postgres:/var/lib/postgresql/data"

  kong-migrations:
    image: kong
    environment:
      - KONG_DATABASE=postgres
      - KONG_PG_HOST=kong-database
      - KONG_PG_PASSWORD=kong
      - KONG_CASSANDRA_CONTACT_POINTS=kong-database
    command: kong migrations bootstrap
    restart: on-failure
    networks:
      - kong-net
    depends_on:
      - kong-database

  kong:
    image: kong
    container_name: kong
    environment:
      - LC_CTYPE=en_US.UTF-8
      - LC_ALL=en_US.UTF-8
      - KONG_DATABASE=postgres
      - KONG_PG_HOST=kong-database
      - KONG_PG_USER=kong
      - KONG_PG_PASSWORD=kong
      - KONG_CASSANDRA_CONTACT_POINTS=kong-database
      - KONG_PROXY_ACCESS_LOG=/dev/stdout
      - KONG_ADMIN_ACCESS_LOG=/dev/stdout
      - KONG_PROXY_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl
    restart: on-failure
    ports:
      - 8000:8000
      - 8443:8443
      - 8001:8001
      - 8444:8444
    links:
      - kong-database:kong-database
    networks:
      - kong-net
    depends_on:
      - kong-migrations


volumes:
  db-data-kong-postgres:

networks:
  kong-net:
    external: false
```

这个yml文件可以直接通过`docker-compose`来加载

```shell
docker-compose -f docker-compose.yml up -d
```

使用httpie(或者curl)来查看运行情况，会返回当前运行的状态，实际上，8001的默认端口是kong的admin接口

> httpie支持多种系统和环境的安装，brew，apt，pypi，dnf，yum，pacman等

```shell
# httpie
http :8001/
# curl
# curl -i http://localhst:8001/
```

kong有四个端口，分别为两个代理端口

1. 8000
2. 8443：ssl

两个admin管理端口

1. 8001
2. 8444：ssl

# 通用认证

一般情况下，上游API服务都需要客户端有身份认证，且不允许错误的认证或无认证的请求通过。认证插件可以实现这一需求。这些插件的通用方案/流程如下：

1. 向一个API或全局添加AUTH插件（此插件不作用于consumers）；

2. 创建一个consumer对象；

3. 为consumer提供指定的验证插件方案的身份验证凭据；

4. 现在，只要有请求进入Kong，都将检查其提供的身份验证凭据（取决于auth类型），如果该请求无法被验证或者验证失败，则请求会被锁定，不执行向上游服务转发的操作。

但是，上述的一般流程并不是总是有效的。譬如，当使用了外部验证方案（比如LDAP）时，KONG就不会（不需要）对consumer进行身份验证。

# Consumers

最简单的理解和配置consumer的方式是，将其于用户进行一一映射，即一个consumer代表一个用户（或应用）。但是对于KONG而言，这些都无所谓。consumer的核心原则是你可以为其添加插件，从而自定义他的请求行为。所以，或许你会有一个手机APP应用，并为他的每个版本都定义一个consumer，又或者你又一个应用或几个应用，并为这些应用定义统一个consumer，这些都无所谓。这是一个模糊的概念，他叫做consumer，而不是user！万万要区分开来，且不可混淆。

# 匿名验证

首先需要创建一个Service来做上有服务，来匹配到相应的相应的转发的目的地，一个Service可以由多个Route，匹配到的Route都会转发给Service。

Service可以是一个世纪的地址，也可以是kong内部提供的upstream object

**使用httpie来创建一个Service**

```shell
# http POST :8001/services name=example host=mocbin.org path=/request
http POST :8001/services/ name=example url=http://mocbin.org/request 
# CURL
# curl -i -X POST http://localhost:8001/services -d name 'name=test.jwt' -d 'host=127.0.0.1' -d 'path=/'
# response:
{
    "client_certificate": null,
    "connect_timeout": 60000,
    "created_at": 1592297652,
    "host": "mocbin.org",
    "id": "702fe513-9155-4b80-8aee-51a242382f4c",
    "name": "example",
    "path": "/request",
    "port": 80,
    "protocol": "http",
    "read_timeout": 60000,
    "retries": 5,
    "tags": null,
    "updated_at": 1592297652,
    "write_timeout": 60000
}
```

**为这个Service开启jwt插件**

```shell
http POST :8001/services/example/plugins name=jwt
# CURL
# curl -i -X POST http://localhost:8001/services/example/plugins -d 'name=jwt'
{
    "config": {
        "anonymous": null,
        "claims_to_verify": null,
        "cookie_names": [],
        "header_names": [
            "authorization"
        ],
        "key_claim_name": "iss",
        "maximum_expiration": 0,
        "run_on_preflight": true,
        "secret_is_base64": false,
        "uri_param_names": [
            "jwt"
        ]
    },
    "consumer": null,
    "created_at": 1592299373,
    "enabled": true,
    "id": "7b9ad3bc-e13a-4bb5-8bab-c1e367b80157",
    "name": "jwt",
    "protocols": [
        "grpc",
        "grpcs",
        "http",
        "https"
    ],
    "route": null,
    "service": {
        "id": "702fe513-9155-4b80-8aee-51a242382f4c"
    },
    "tags": null
}
```

**创建一个属于这个Service的Route**

```shell
http POST :8001/services/example/routes paths:='["/auth-sample"]' name=auth-route
# CURL
# curl -i -X POST http://localhost:8001/services/example/routes -d 'paths[]=/auth-sample' -d 'name=auth-route'
# response:
{
    "created_at": 1592299628,
    "destinations": null,
    "headers": null,
    "hosts": null,
    "https_redirect_status_code": 426,
    "id": "bf202b62-ee80-4758-a13c-15ad7b6f8054",
    "methods": null,
    "name": "auth-route",
    "path_handling": "v0",
    "paths": [
        "/auth-sample"
    ],
    "preserve_host": false,
    "protocols": [
        "http",
        "https"
    ],
    "regex_priority": 0,
    "service": {
        "id": "702fe513-9155-4b80-8aee-51a242382f4c"
    },
    "snis": null,
    "sources": null,
    "strip_path": true,
    "tags": null,
    "updated_at": 1592299628
}
```

现在让我们常识访问我们绑定的path

```shell
http :8000/auth-sample
# CURL
# curl -i -X GET http://localhost:8000/auth-sample
# response:
{
    "message": "Unauthorized"
}
```

**创建一个consumer**

```shell
http POST :8001/consumers/ username=example.jwt
# CURL
# curl -i -X POST http://localhost:8001/consumers/ -d 'username=example.jwt'
# response:
{
    "created_at": 1592299896,
    "custom_id": null,
    "id": "cd2b2a31-92a6-4f89-a7b1-dc970543cc34",
    "tags": null,
    "username": "example.jwt"
}
```

**为刚才创建的consumer申请一个jwt凭证**

可以指定算法`algorith`，`iss`签发这key，秘钥`secret`，也可以省略，让kong自动生成

```shell
http :8001/consumers/example.jwt/jwt algorithm=HS256 key=custom_key secret=customsecretkey
# CURL
# curl -i -X POST http://localhost:8001/consumers/example.jwt/jwt -d 'algorithm=HS256' -d 'key=custom_key' -d 'secret=customsecretkey'
# response:
{
    "algorithm": "HS256",
    "consumer": {
        "id": "cd2b2a31-92a6-4f89-a7b1-dc970543cc34"
    },
    "created_at": 1592300159,
    "id": "e3fc30d7-e48a-47a9-b622-0e8c1e8e9be3",
    "key": "custom_key",
    "rsa_public_key": null,
    "secret": "customsecretkey",
    "tags": null
}
```

查看刚刚创建的example jwt的凭证

```shell
http :8001/consumers/example.jwt/jwt
# CURL
# curl -i -X GET http://localhost:8001/consumers/example.jwt/jwt
# response:
{
    "data": [
        {
            "algorithm": "HS256",
            "consumer": {
                "id": "cd2b2a31-92a6-4f89-a7b1-dc970543cc34"
            },
            "created_at": 1592300159,
            "id": "e3fc30d7-e48a-47a9-b622-0e8c1e8e9be3",
            "key": "custom_key",
            "rsa_public_key": null,
            "secret": "customsecretkey",
            "tags": null
        }
    ],
    "next": null
}
```

现在可以进行jwt下发了

业务服务器根据kong生成的jwt凭证中的`algorithm、key（iss）、secret`进行`token`的演算和下发。请求`鉴权接口`需携带`Authorization: Bearer {jwt}`进行请求。测试的话可以用 [https://jwt.io](https://jwt.io/) 生成：

![](http://img.lte.ink/Xnip2020-06-16_17-46-34.png)

`iss`为申请jwt认证时设置的key，`alg`为加密算法，加上自定义的`customsecretkey`，在左侧生成了一个jwt token

```shell
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJjdXN0b21fa2V5In0.6bzcpDKkZMHlnSlm9H1-5Uz-4l4MWvrRicUbvdMfotg
```

请求带有jwt认证服务的路由

```shell
http :8000/auth-sample 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJjdXN0b21fa2V5In0.6bzcpDKkZMHlnSlm9H1-5Uz-4l4MWvrRicUbvdMfotg'
# CURL
# curl -i -X http://localhost:8000/auth-sample -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJpc3MiOiJjdXN0b21fa2V5In0.6bzcpDKkZMHlnSlm9H1-5Uz-4l4MWvrRicUbvdMfotg'
```

返回的是我们绑定的目标页面，这里拿bing做了一个示例

```shell
HTTP/1.1 200 OK
Cache-Control: private, max-age=0
Connection: keep-alive
Content-Encoding: gzip
Content-Length: 46129
Content-Type: text/html; charset=utf-8
Date: Tue, 16 Jun 2020 10:03:08 GMT
P3P: CP="NON UNI COM NAV STA LOC CURa DEVa PSAa PSDa OUR IND"
Set-Cookie: SRCHD=AF=NOFORM; domain=.bing.com; expires=Thu, 16-Jun-2022 10:03:08 GMT; path=/
Set-Cookie: SRCHUID=V=2&GUID=4209CB1955834EECABE0207953B577D3&dmnchg=1; domain=.bing.com; expires=Thu, 16-Jun-2022 10:03:08 GMT; path=/
Set-Cookie: SRCHUSR=DOB=20200616; domain=.bing.com; expires=Thu, 16-Jun-2022 10:03:08 GMT; path=/
Set-Cookie: _SS=SID=05D8560E0A126FB1338C58E50B3C6E81; domain=.bing.com; path=/
Set-Cookie: _EDGE_S=F=1&SID=05D8560E0A126FB1338C58E50B3C6E81; path=/; httponly; domain=bing.com
Set-Cookie: _EDGE_V=1; path=/; httponly; expires=Sun, 11-Jul-2021 10:03:08 GMT; domain=bing.com
Set-Cookie: MUID=31B1C11B0EBF6ED21483CFF00F916F99; samesite=none; path=/; secure; expires=Sun, 11-Jul-2021 10:03:08 GMT; domain=bing.com
Set-Cookie: MUIDB=31B1C11B0EBF6ED21483CFF00F916F99; path=/; httponly; expires=Sun, 11-Jul-2021 10:03:08 GMT
Vary: Accept-Encoding
Via: kong/2.0.4
X-Kong-Proxy-Latency: 209
X-Kong-Upstream-Latency: 91
X-MSEdge-Ref: Ref A: A6861B412B984BCBB0AE5543A57C648D Ref B: BJ1EDGE0117 Ref C: 2020-06-16T10:03:08Z
```


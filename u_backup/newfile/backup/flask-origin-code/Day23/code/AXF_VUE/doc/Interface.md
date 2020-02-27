# Interface

## User
- /users/
- post
- 参数（get, query_params）
    - action
        - login
        - register
        - checkusername
- 提交参数
    - register
        - u_name
        - u_password
        - u_email
    - login
        - u_user
        - u_password
        
## Goods
- /markets/goods/
- get


## Carts
- /carts/
- get
    - token
- post
    - token
    - goodsid
    
    
## 扫码登录
- 前提条件
    - 二维码
    - 能扫码的客户端
        - 账号登录好的
    - 网页端登录
- 扫描网页上的二维码实现了网页上用户的登录
- 二维码中存储的是登录的链接
    - 特殊的登录链接
    - 使用token登录的
- 网页会在手机点击确认后，跳转到登录
    - 长连接
    - 周期性请求    
    
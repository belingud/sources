# 亚马逊云服务AWS一锤一锤搭梯子

## 创建实例

亚马逊的云服务比阿里云还要好一点，现在亚马逊服务器有一年的免费体验，依托于此，用shadowsocks来实现代理上网。不过也是有限制的，每月100w次请求，15G流量。

1. 首先是注册亚马逊账号，注册信息可以随便填，可以填真实信息。需要一张信用卡，国内国外皆可，会预扣除1美元，超出15G之后才会扣费，不提醒。建议使用淘宝aws EC2虚拟卡。
2. 填写手机号，邮箱，会收到一封确认邮件，点击完成确认即可。
2. 创建实例，即服务器主机。进入主页，点击我的账户，进入AWS控制台，选择创建实例。
3. 在列表里面选择EC2，如果提示信息错误，就重新填写，注意选择地区和主机需要是免费，建议使用ubuntu16，日本的主机，基础配置就好了。
4. 创建完成，审核启动，会让你生成一个秘钥，并下载到本地。
5. 启动实例后，点击左上放的连接，根据官方教程连接你的实例，需要用到秘钥对。

连接不需要密码，载入秘钥对就能成功连接，连接成功后可以根据自己需求更改密码，`passwd ubuntu`，然后根据提示改密码。

## 安装软件

1. 提升权限，安装软件
1. sudo -s，进入root用户
1. apt update，更新软件源
1. apt install python3-pip，安装python包管理工具
1. pip3 install shadowsocks，安装科学上网软件
  - pip库中的shadowsocks已经不再维护，只更新到2.8版本
  - 如果想安装最新的3.0版本，需要下载压缩包可后自行安装
  - wget –no-check-certificate -O shadowsocks-master.zip https://github.com/shadowsocks/shadowsocks/archive/master.zip 下载
  - pip install shadowsocks-master.zip
  - systemctl start shadowsocks 启动服务
  - ssserver –version 可以查看当前版本。

可以安装锐速和BBR加速访问速度，锐速不支持最新的内核，需要降到3.15，BBR需要4.9以上内核，如何配置之后会补充。

## 配置shadowsocks

编写一个配置文件，在/etc/shadowsocks.json中编写配置（如果没有就创建）

单用户配置:
    {
        "server":"0.0.0.0",
        "server_port":"9229",
        "local_address":"127.0.0.1",
        "local_port":"1080",
        "password":"自己的密码",
        "timeout":500,
        "method":"aes-256-cfb",
        "fast_open":false
    }

多用户配置:
    {
        "server":"0.0.0.0",
        "server_port":"9229",
        "local_address":"127.0.0.1",
        "local_port":"1080",
        "port_password":{
            "9229":"密码",
            "9230":"密码",
            "9231":"密码"
        }
        "timeout":500,
        "method":"aes-256-cfb",
        "fast_open":false
    }

一般单用户就够了，可以在多台设备登录。

## 启动配置

1. 在终端中启动服务器ssserver -c /etc/shadowsocks.json
1. 加入开机自启，编辑/etc/rc.local ，将启动指令粘贴到此
1. 去服务器配置中打开端口，到自己的实例上，到最右边找到安全组，进入安全组设置，点击左下角的入站，编辑，点击添加规则，在端口范围里填上我们设置的端口，来源下拉框中选择任何位置。

## 连接使用

1. 在Android手机上可以使用影梭进行连接

1. 在mac，linux，windows上可以使用shadowsocks客户端，都是开源的

1. windows版本https://github.com/shadowsocks/shadowsocks-windows

1. linux，mac版本https://github.com/shadowsocks/shadowsocks-qt5

1. android版本https://github.com/shadowsocks/shadowsocks-android






### 安装

redis官网：<https://redis.io/>

点击上方的**Download**，在下方的下载按钮点击右键，复制下载链接。在命令行输入`wget 下载链接 保存目录`

```shell
wget http://download.redis.io/releases/redis-5.0.5.tar.gz
```



下载一个后缀为.tar.gz的压缩包。进入到下载的目录中，命令行运行`tar xvzf redis-5.0.5.tar.gz`，完成解压，自动创建一个同名目录

进入目录下：`cd redis-5.0.5.tar.gz`，运行`make`，完成后运行`make test`进行测试。

进入安装文件的目录：`cd redis-5.0.5.tar.gz/utils `，运行安装脚本`./install_server.sh`，运行失败则使用bash命令运行`bash install_server.sh`，等待安装完成。

### 配置

安装完成后需要对redis进行配置，使其支持远程链接，或者将其加入到服务器族群中，配置文件在`/etc/redis/6379.conf`中，在命令模式下输入`/bind`，找到`bind 127.0.0.1`，将其注释掉。使服务器的redis服务支持远程链接。

如果你的redis需要密码，在命令模式下输入`/requirepass foobared`，回车，按<kbd>N</kbd>键依次查找，找到

```shell
# requirepass foobared
```

的一行，删除注释，将后面的foobared替换为你需要修改的密码，保存退出。

重启redis服务`service redis-server restart`


# Docker



Docker 是一个开元的应用容器引擎,开发者可以打包应用到一个可移植的镜像中,发布到任何运行Linux或Ubuntu的机器上,也可以实现虚拟化.容器是完全使用沙箱机制,相互之间不会有任何接口.



类似于虚拟机,docker实现了容器内和容器外以及容器间的相对独立,容器内外通过不同的端口进行通信.但是Docker的性能比一般的虚拟机高出很多.正是因为Docker的性能,才让它流行起来.



使用Docker在服务器上部署项目只需要几个简单的命令,使用`docker push`将镜像推到服务器,根据镜像名就可以启动镜像.



docker常用的操作,包括打包镜像,启动镜像,推送镜像和查看信息.



docker常用命令:



```shell
# build打包成image镜像
# .表示在当前目录下
docker build -t image_name:v1 .
# 启动docker镜像
docker run image_name:v1
docker run -d image_name:v1 # -d参数表示在后台运行
docker run -it image_name:v1 # -it表示进入docker镜像的虚拟命令行
# 查看正在运行的docker镜像
docker ps
# 进入正在运行的docker镜像,运行bash命令
docker exec -it image_id bash
# 查看所有的docker镜像
docker ps -a
# 根据ID启动镜像
docker start ID
# 杀死某个镜像
docker kill ID
# 停止某个镜像的运行
docker stop ID
# 查看docker所有镜像
docker images
# 杀死所有docker镜像
docker kill $(docker ps -q)
# docker删除某个镜像
docker rmi [image]
docker image rm [image]
# 清理镜像文件,会将没有被引用的镜像文件全部删除
docker image prune
```



docker可以修改配置文件,让docker 的根目录指向一个空间大的目录,目录不存在会自动创建,创建的目录属于root用户.你可以用`df -h`来查看磁盘占用情况,来决定是否需要更换docker目录.



使用`docker info`来查看docker信息,可以看到`Docker Root Dir`的一项,即是docker的根目录.



docker根目录修改步骤:



首先进入docker 的配置文件目录`/etc/docker`,创建并编辑一个新的文件`vim daemon.json`,在其中填加以下内容



```json
{
    // graph的值就是你需要更改的docker挂载的根目录
    "graph": "/home/user/docker"
}
```



然后重启docker服务`systemctl restart docker.service`.重启服务后用`docker info`来查看是否修改成功.



# docker-compose



Docker Compose是一个用来定义和运行复杂应用的Docker工具。一个使用Docker容器的应用，通常由多个容器组成。使用Docker Compose不再需要使用shell脚本来启动容器。 
Compose 通过一个配置文件来管理多个Docker容器，在配置文件中，所有的容器通过services来定义，然后使用docker-compose脚本来启动，停止和重启应用，和应用中的服务以及所有依赖服务的容器，非常适合组合使用多个容器进行开发的场景。



docker-compose使用YAML文件来写配置.



>YAML是一种表示序列化数据的格式,用空格来表示层级关系,简单易懂



`docker-compose.yml`文件:



```yml
version: "3"
services:
 
  redis:
    image: redis:alpine
    ports:
      - "6379"
    networks:
      - frontend
    deploy:
      replicas: 2
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure
 
  db:
    image: postgres:9.4
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    deploy:
      placement:
        constraints: [node.role == manager]
 
  vote:
    image: dockersamples/examplevotingapp_vote:before
    ports:
      - 5000:80
    networks:
      - frontend
    depends_on:
      - redis
    deploy:
      replicas: 2
      update_config:
        parallelism: 2
      restart_policy:
        condition: on-failure
 
  result:
    image: dockersamples/examplevotingapp_result:before
    ports:
      - 5001:80
    networks:
      - backend
    depends_on:
      - db
    deploy:
      replicas: 1
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure
 
  worker:
    image: dockersamples/examplevotingapp_worker
    networks:
      - frontend
      - backend
    deploy:
      mode: replicated
      replicas: 1
      labels: [APP=VOTING]
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 3
        window: 120s
      placement:
        constraints: [node.role == manager]
 
  visualizer:
    image: dockersamples/visualizer:stable
    ports:
      - "8080:8080"
    stop_grace_period: 1m30s
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      placement:
        constraints: [node.role == manager]
 
networks:
  frontend:
  backend:
 
volumes:
  db-data:
```



安装docker-compose



```shell
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```



docker-compose 命令

```shell
# 启动docker服务,将docker镜像push到镜像服务器,-d表示在后台运行
docker-compose -f docker-compose.yml up -d
# 关闭docker服务
docker-compose -f docker-compose.yml down
```



DOCKERFILE是用来构建docker镜像的文件,固定命名`Dockerfile`,是由一系列命令和参数构成的脚本,精简了镜像从头到尾的创建流程极大地简化了部署工作.



Dockerfile从FROM命令开始,紧接着跟随着各种方法,命令和参数.



Dockerfile的常用语法:



```dockerfile
# FROM表示镜像运行的系统环境
FROM ubuntu:18.04
# RUN 可以执行系统命令行
RUN apt-get update
# RUN命令是在生成docker image时候执行的命令
RUN mkdir /code
# COPY将文件拷贝到指定的目录
COPY requirements.txt /code
RUN locale-gen en_US.UTF-8

# 配置环境变量,Dockerfile里面不能使用修改.bashrc的方式更改环境变量
# 格式: ENV KEY VALUE
ENV LANG en_US.utf8
ENV LC_LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# 切换工作路径,Dockerfile里面不能使用cd命令
WORKDIR /code

# CMD为镜像启动时候执行的命令
CMD ["sh","-c", "python3 manage.py collectstatic"]
```



理解Dockerfile最关键的是理解生成镜像时的路径问题.



利用Dockerfile生成docker镜像,生成FROM所对应的文件目录,docker工作路径下的文件不会自动复制到镜像中,只有COPY命令会将文件复制.docker镜像中的目录和docker的工作路径需要有明确的概念.



主要区别在于RUN,RUN执行的命令是在docker镜像里面执行的,COPY命令是在当前路径下执行的.


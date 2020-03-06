FROM ubuntu:18.04
RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list && apt update && apt install -y curl zsh git vim wget 
COPY env_init.sh /
WORKDIR /
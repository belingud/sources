FROM ubuntu:18.04
RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list && apt-get update && \
    apt-get install -y --no-install-recommends curl zsh git vim wget && apt-get clean && apt-get autoclean
COPY env_init.sh /root
COPY .zshrc /root/.zshrc
WORKDIR /root

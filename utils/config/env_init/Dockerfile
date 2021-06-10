# 可以使用php镜像作为开发环境，如果原始镜像无法满足开发环境的依赖，可以考虑重写新的Dockerfile来安装新的依赖
# 起始镜像，作为底包
FROM php:7.2-fpm-alpine
LABEL maintainer="flower"
# 安装xhprof依赖
RUN apk add gcc g++ make libffi-dev openssl-dev libtool m4 autoconf --no-cache && pecl install xhprof

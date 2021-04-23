FROM phpstorm/php-72-cli-xdebug-27
LABEL maintainer=belingud
RUN sed -i -e "s/\/\/archive\.ubuntu/\/\/mirrors.aliyun/" /etc/apt/sources.list && \
    apt update && apt install -y --no-install-recommends libpng-dev && docker-php-ext-install pdo pdo_mysql gd
RUN pecl install xhprof
# RUN echo 'xdebug.remote_enable=1' >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
#     echo 'xdebug.remote_host=host.docker.internal' >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
#     echo 'xdebug.remote_port=9000' >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
#     echo 'xdebug.idekey=PHPSTORM' >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini


FROM php:8.1-fpm

# 更换镜像源并安装依赖
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    libonig-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        gd \
        pdo \
        pdo_mysql \
        mysqli \
        mbstring \
        zip \
        curl \
        exif \
        bcmath \
    && pecl install redis \
    && docker-php-ext-enable redis

# 后续步骤
WORKDIR /var/www/html/project
COPY project /var/www/html/project/
RUN chown -R www-data:www-data /var/www/html/project \
    && chmod -R 755 /var/www/html/project

EXPOSE 9000
CMD ["php-fpm"]

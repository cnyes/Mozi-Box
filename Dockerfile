FROM php:7.1-cli-alpine

LABEL maintainer="Cnyes Backend Team <rd-backend@cnyes.com>"

WORKDIR /srv/app

ENV COMPOSER_ALLOW_SUPERUSER 1

COPY ./ /srv/app
COPY --from=composer /usr/bin/composer /usr/bin/composer

RUN apk update && \
    apk add ${PHPIZE_DEPS} && \
    pecl install xdebug && \
    docker-php-ext-enable xdebug && \
    composer install --no-interaction --no-progress --no-suggest --no-ansi --prefer-dist --optimize-autoloader && \
    echo "phar.readonly = Off" > /usr/local/etc/php/conf.d/custom.ini

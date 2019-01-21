#### build stages ####

FROM php:7.1-cli-alpine AS build-stage

WORKDIR /srv/app

ENV COMPOSER_ALLOW_SUPERUSER 1

COPY ./ /srv/app
COPY --from=composer /usr/bin/composer /usr/local/bin/composer

RUN apk update && \
    apk add make python2 py2-pip && \
    pip install wheel && \
    chmod +x /usr/local/bin/composer && \
    echo "phar.readonly = Off" > /usr/local/etc/php/conf.d/custom.ini && \
    cd /srv/app/src/bitbucket-cli || exit 1 && \
    composer install --no-interaction --no-dev --no-progress --no-suggest --no-ansi --prefer-dist --optimize-autoloader && \
    ./bitbucket-cli app:build -q bitbucket-cli && \
    mkdir -p /srv/app/dist && \
    cp ./builds/bitbucket-cli /srv/app/dist && \
    cd /srv/app/src/deployfish-ext || exit 1 && \
    make dist && \
    cp ./dist/deployfish-ext-0.0.1.tar.gz /srv/app/dist && \
    cp -rp /srv/app/src/tools-install /srv/app/dist

#### final stages ####

FROM php:7.1-cli-alpine

LABEL maintainer="Cnyes Backend Team <rd-backend@cnyes.com>"

ENTRYPOINT []

COPY --from=build-stage /srv/app/dist /tmp/dist/

RUN sh /tmp/dist/tools-install/install.sh

ENV PATH=${PATH}:/google-cloud-sdk/bin

COPY ./src/scripts /scripts

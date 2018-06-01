FROM php:7.1-cli-alpine

LABEL maintainer="Cnyes Backend Team <rd-backend@cnyes.com>"

RUN export terraform_version=0.11.7 && \
    apk add --no-cache python2 py2-pip jq git && \
    pip install deployfish==0.19.1 requests && \
    cd /tmp || exit 1 && \
    wget -O ./terraform.zip https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip && \
    unzip ./terraform.zip && \
    mv terraform /usr/local/bin && \
    chmod +x /usr/local/bin/terraform && \
    rm ./terraform.zip

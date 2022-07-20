FROM nginx:1.23.0-alpine

LABEL maintainer="yinjingyu270@berrygenomics.com"

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG CHANGE_SOURCE=false
RUN if [ ${CHANGE_SOURCE} = true ]; then \
    # Change application source from dl-cdn.alpinelinux.org to aliyun source
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/' /etc/apk/repositories \
;fi

RUN apk update \
    && apk upgrade \
    && apk --update add logrotate \
    && apk add --no-cache openssl \
    && apk add --no-cache bash

RUN apk add --no-cache curl

RUN set -x ; \
    addgroup -g 1000 -S pyflask ; \
    adduser -u 1000 -D -S -G pyflask pyflask && exit 0 ; exit 1


# ADD ./nginx.conf /etc/nginx/

CMD ["nginx"]

EXPOSE 80 81 443
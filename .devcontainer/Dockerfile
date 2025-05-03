# build時に使用するARGを定義している部分
ARG ubuntu_version
ARG timezone
ARG port_web_server

# https://hub.docker.com/_/ubuntu/
FROM ubuntu:${ubuntu_version}

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=ja_JP.UTF-8
ENV LC_CTYPE=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:jp
ENV TZ $timezone
ENV PORT_WEB_SERVER $port_web_server
ENV APP_CODE_PATH_CONTAINER $app_code_path_container

# Ubuntu base setting (locale と timezone と デバッグによく使用するものを入れる)
RUN sed -i'' 's/archive.ubuntu.com/jp.archive.ubuntu.com/' /etc/apt/sources.list
RUN apt-get update \
    && apt-get -y -q install \
    # Lang ja
    # language-pack-ja-base language-pack-ja apt-transport-https \
    # devtool
    vim netcat git curl wget zip unzip sudo net-tools \
    # pkg-config libgtk-3-dev cmake ninja-build gnupg gcc libc-dev clang software-properties-common \
    python3-pip libnss3 libpq-dev postgresql-client

# python requirements
COPY ./requirements.txt /tmp/requirements.txt
RUN ln -s /bin/python3.8 /bin/python \
    && pip install -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

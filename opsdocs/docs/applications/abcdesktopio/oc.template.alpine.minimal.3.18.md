# oc.template.alpine.minimal.3.18
## from
 Docker official images [alpine:3.18](https://hub.docker.com/_/alpine)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.18.11
PRETTY_NAME="Alpine Linux v3.18"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"

```



## `DockerFile` source code

``` 

ARG BASE_IMAGE=alpine
FROM ${BASE_IMAGE}

MAINTAINER Alexandre DEVELY 
RUN mkdir -p /composer/init.d
COPY etc/ /etc

ENV TERM linux


# add core lib and bin
RUN  apk add --no-cache 		\
     gnupg                              \
     cups-client			\
     libpulse				\
     curl				\
     openssl				\
     xauth

ENV LANG en_US.utf8

############
COPY composer /composer

RUN apk add --no-cache --update bash nodejs npm

# Add nodejs service
RUN cd /composer/node/ocrun 	 && npm install  
# RUN cd /composer/node/ocdownload && npm install


##########
# Next command use $BUSER context
ENV BUSER balloon
ENV BGROUP balloon
ENV BUID 4096
ENV BGID 4096
# RUN adduser --disabled-password --gecos '' $BUSER
# RUN id -u $BUSER &>/dev/null || 
RUN addgroup --gid $BGID $BGROUP
RUN adduser -D -h /home/balloon -s /bin/sh -u $BUID -G balloon $BUSER

# create an ubuntu user
# PASS=`pwgen -c -n -1 10`
# PASS=ballon
# Change password for user balloon

# if --build-arg BUILD_BALLON_PASSWORD=1, set NODE_ENV to 'development' or set to null otherwise.
#ENV BALLOON_PASSWORD=${BUILD_BALLOON_PASSWORD:+development}
# if BUILD_BALLOON_PASSWORD is null, set it to 'abcdesktop' (or leave as is otherwise).
#ENV BALLOON_PASSWORD=${BUILD_BALLOON_PASSWORD:-abcdesktop}

RUN echo "balloon:lmdpocpetit" | chpasswd $BUSER

RUN mkdir -p /var/log/desktop && \
    chown -R $BUSER:$BUSER /home/$BUSER /var/log/desktop

```



> file oc.template.alpine.minimal.3.18.md is created at Tue Jan 28 2025 13:48:59 GMT+0000 (Coordinated Universal Time) by make-docs.js

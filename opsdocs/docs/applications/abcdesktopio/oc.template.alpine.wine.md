# oc.template.alpine.wine
## from
 inherit [abcdesktopio/oc.template.alpine](../oc.template.alpine)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.19.1
PRETTY_NAME="Alpine Linux v3.19"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"

```



## `DockerFile` source code

``` 

# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

# 
# from https://wiki.alpinelinux.org/wiki/Repositories#Enabling_the_community_repository
#
# RUN echo https://dl-cdn.alpinelinux.org/alpine/v$(cut -d'.' -f1,2 /etc/alpine-release)/main/ >> /etc/apk/repositories && \
#    echo https://dl-cdn.alpinelinux.org/alpine/v$(cut -d'.' -f1,2 /etc/alpine-release)/community/ >> /etc/apk/repositories && \
#    echo https://dl-cdn.alpinelinux.org/alpine/edge/testing/ >> /etc/apk/repositories 


#
# add wine
#
# wine packge does not exist on alpine aarch64
# install only x86_64 architecture
RUN if [ $(uname -m) == 'aarch64' ]; then echo 'WARNING wine package does not exist on alpine aarch64'; fi
RUN if [ $(uname -m) == 'x86_64'  ]; then apk add --no-cache --update wine; fi

```



> file oc.template.alpine.wine.md is created at Tue Mar 26 2024 09:13:58 GMT+0000 (Coordinated Universal Time) by make-docs.js

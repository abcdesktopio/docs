# oc.template.rockylinux.nvidia.8
## from
 inherit [nvidia/cuda:12.4.1-base-rockylinux8](../cuda)
## Container distribution release


``` 
NAME="Rocky Linux"
VERSION="8.10 (Green Obsidian)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="8.10"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Rocky Linux 8.10 (Green Obsidian)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:8:GA"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2029-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-8"
ROCKY_SUPPORT_PRODUCT_VERSION="8.10"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="8.10"

```



## `DockerFile` source code

``` 
ARG BASE_IMAGE=rockylinux:8
FROM ${BASE_IMAGE}

MAINTAINER Alexandre DEVELY

RUN mkdir -p /composer/init.d
COPY etc/ /etc


RUN  dnf update -y && \
     dnf install -y --allowerasing \
     glibc-langpack-en \
     cups-client \
     pulseaudio-libs \
     curl \
     xorg-x11-xauth \
     && dnf -y clean all \
     && rm -rf /var/cache 

ENV LANG en_US.utf8

COPY composer /composer

RUN    dnf update -y \
    && dnf module -y enable nodejs:18 \
    && dnf install -y nodejs \ 
    && dnf clean -y all \
    && rm -rf /var/cache

# Add nodejs service
RUN cd /composer/node/ocrun 	 && npm install  
# RUN cd /composer/node/ocdownload && npm install


##########
# Next command use $BUSER context
ENV BUSER balloon
# RUN adduser --disabled-password --gecos '' $BUSER
# RUN id -u $BUSER &>/dev/null || 
RUN groupadd --gid 4096 $BUSER
RUN useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups $BUSER $BUSER
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



> file oc.template.rockylinux.nvidia.8.md is created at Tue Jan 28 2025 13:55:08 GMT+0000 (Coordinated Universal Time) by make-docs.js

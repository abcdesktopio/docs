# oc.template.ubuntu.nvidia.22.04
## from
 inherit [nvidia/cuda:12.0.0-base-ubuntu22.04](../cuda)
## Container distribution release


``` 
PRETTY_NAME="Ubuntu 22.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy

```



## `DockerFile` source code

``` 
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

MAINTAINER Alexandre DEVELY 
RUN mkdir -p /composer/init.d
COPY etc/ /etc

# correct debconf: (TERM is not set, so the dialog frontend is not usable.)
ENV DEBCONF_FRONTEND noninteractive
ENV TERM linux
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get install -y --no-install-recommends \
     gnupg \
     software-properties-common \
     locales \
     cups-client \
     libpulse0 \
     curl \
     xauth \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/ \
     && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
# default LANG is en_US
ENV LANG en_US.utf8

# copy compser source code
COPY composer /composer

# install nodejs and npm
# the default install version is 20
#
# read from https://github.com/nodesource/distributions
#
# | Distro Name          | Node 16x | Node 18x | Node 20x |
# | :------------------- | :------: | :------: | :------: |
# | Ubuntu Bionic ^18.04 |    OK    |    KO    |    KO    |
# | Ubuntu Focal ^20.04  |    OK    |    OK    |    OK    |
# | Ubuntu Jammy ^22.04  |    OK    |    OK    |    OK    |
#
# if VERSION_ID == 18.04 then install nodejs 16 else install nodejs 20
RUN NODE_MAJOR=20; if [ "18.04" = "$(. /etc/os-release;echo $VERSION_ID)" ]; then NODE_MAJOR=16; fi; echo "node version install $NODE_MAJOR" && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \ 
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add nodejs service
# ocrun can call create another container or pod
RUN cd /composer/node/ocrun && npm install  

#
# create account 
# Next command use $BUSER context
# this is the default user if no user defined
ENV BUSER balloon
# create group, user, set password
RUN groupadd --gid 4096 $BUSER && \
    useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups $BUSER $BUSER && \
    echo "balloon:lmdpocpetit" | chpasswd $BUSER
# allow default user to write in /var/log/desktop  if no user defined 
RUN mkdir -p /var/log/desktop && \
    chown -R $BUSER:$BUSER /home/$BUSER /var/log/desktop


```



> file oc.template.ubuntu.nvidia.22.04.md is created at Wed May 01 2024 13:22:55 GMT+0000 (Coordinated Universal Time) by make-docs.js

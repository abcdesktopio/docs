# oc.template.ubuntu.minimal.20.04
## from
 Docker official images [ubuntu:20.04](https://hub.docker.com/_/ubuntu)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="20.04.5 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.5 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal

```



## `DockerFile` source code

``` 

ARG BASE_IMAGE=ubuntu:20.04
FROM ${BASE_IMAGE}

MAINTAINER Alexandre DEVELY 
RUN mkdir -p /composer/init.d
COPY etc/ /etc

# correct debconf: (TERM is not set, so the dialog frontend is not usable.)
ENV DEBCONF_FRONTEND noninteractive
ENV TERM linux
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get install -y --no-install-recommends \
     gnupg                              \
     software-properties-common         \
     locales				\
     cups-client			\
     libpulse0				\
     curl				\
     xauth				\
     && apt-get clean			\
     && rm -rf /var/lib/apt/lists/	\
     && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

############
COPY composer /composer

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - \
        && apt-get update &&                            \
        apt-get install -y --no-install-recommends      \
                nodejs                                  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



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


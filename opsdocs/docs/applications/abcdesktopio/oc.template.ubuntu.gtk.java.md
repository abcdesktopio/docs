# oc.template.ubuntu.gtk.java
## from
 inherite [abcdesktopio/oc.template.ubuntu.gtk.20.04](../oc.template.ubuntu.gtk.20.04)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
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
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:$TAG
MAINTAINER Alexandre DEVELY 
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --install-recommends \
        default-jre	\
        gsfonts-x11   	\
    && rm -rf /var/lib/apt/lists/*	

```


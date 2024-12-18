# oc.template.ubuntu.gtk.language-pack-all
## from
 inherite [abcdesktopio/oc.template.ubuntu.gtk](../oc.template.ubuntu.gtk)
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
# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

ENV DEBIAN_FRONTEND noninteractive  
# install help in all languages for gnome
#RUN apt-get update && apt-get install -y  --no-install-recommends       \
#        $(apt-cache search language-pack-gnome | awk '{print $1 }')                \
#        && rm -rf /var/lib/apt/lists/*
#
#
#
RUN apt-get update && apt-get install -y  --no-install-recommends       				\
        $(apt-cache search "language-pack-" | grep -v "gnome" | grep -v "kde" | awk '{print $1 }')      \
        && apt-get clean  										\
        && rm -rf /var/lib/apt/lists/*


```


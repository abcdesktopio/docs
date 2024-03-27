# oc.template.rockylinux.8
## from
 inherit [abcdesktopio/oc.template.rockylinux.minimal.8](../oc.template.rockylinux.minimal.8)
## Container distribution release


``` 
NAME="Rocky Linux"
VERSION="8.9 (Green Obsidian)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="8.9"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Rocky Linux 8.9 (Green Obsidian)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:8:GA"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2029-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-8"
ROCKY_SUPPORT_PRODUCT_VERSION="8.9"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="8.9"

```



## `DockerFile` source code

``` 

# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

# add some fonts
RUN yum update -y && \
    yum install -y \
        google-noto-fonts-common \
        xorg-x11-fonts-100dpi \
        xorg-x11-fonts-75dpi \
	texlive-utopia \
	liberation-fonts-common \
     && yum -y clean all \
     && rm -rf /var/cache

```



> file oc.template.rockylinux.8.md is created at Wed Mar 27 2024 20:46:36 GMT+0000 (Coordinated Universal Time) by make-docs.js

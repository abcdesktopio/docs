# oc.template.rockylinux.9
## from
 inherit [abcdesktopio/oc.template.rockylinux.minimal.9](../oc.template.rockylinux.minimal.9)
## Container distribution release


``` 
NAME="Rocky Linux"
VERSION="9.3 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.3"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.3 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.3"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.3"

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



> file oc.template.rockylinux.9.md is created at Thu May 02 2024 15:02:25 GMT+0000 (Coordinated Universal Time) by make-docs.js

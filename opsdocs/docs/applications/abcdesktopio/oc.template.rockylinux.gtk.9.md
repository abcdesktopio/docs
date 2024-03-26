# oc.template.rockylinux.gtk.9
## from
 inherit [abcdesktopio/oc.template.rockylinux.9](../oc.template.rockylinux.9)
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

# install gtk lib
RUN yum update && \
     yum install -y \
        gtk3 \
     && yum -y clean all \
     && rm -rf /var/cache

COPY --from=abcdesktopio/oc.themes /usr/share/icons  /usr/share/icons
COPY --from=abcdesktopio/oc.themes /usr/share/themes /usr/share/themes

```



> file oc.template.rockylinux.gtk.9.md is created at Tue Mar 26 2024 09:37:34 GMT+0000 (Coordinated Universal Time) by make-docs.js

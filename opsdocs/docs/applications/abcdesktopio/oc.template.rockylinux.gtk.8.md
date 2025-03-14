# oc.template.rockylinux.gtk.8
## from
 inherit [abcdesktopio/oc.template.rockylinux.8](../oc.template.rockylinux.8)
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
# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG} 

# install gtk lib
RUN yum update && \
     yum install -y \
        gtk3 \
        gnome-font-viewer \
     && yum -y clean all \
     && rm -rf /var/cache

COPY --from=abcdesktopio/oc.themes /usr/share/icons  /usr/share/icons
COPY --from=abcdesktopio/oc.themes /usr/share/themes /usr/share/themes

```



> file oc.template.rockylinux.gtk.8.md is created at Tue Jan 28 2025 14:08:00 GMT+0000 (Coordinated Universal Time) by make-docs.js

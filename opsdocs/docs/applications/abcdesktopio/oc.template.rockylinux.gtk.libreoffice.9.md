# oc.template.rockylinux.gtk.libreoffice.9
## from
 inherit [abcdesktopio/oc.template.rockylinux.gtk.9](../oc.template.rockylinux.gtk.9)
## Container distribution release


``` 
NAME="Rocky Linux"
VERSION="9.5 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.5"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.5 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
VENDOR_NAME="RESF"
VENDOR_URL="https://resf.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.5"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.5"

```



## `DockerFile` source code

``` 
ARG TAG
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG} 

# install gtk lib
RUN yum update && \
     yum install -y --skip-broken libreoffice \
     && yum -y clean all \
     && rm -rf /var/cache

```



> file oc.template.rockylinux.gtk.libreoffice.9.md is created at Tue Jan 28 2025 14:18:17 GMT+0000 (Coordinated Universal Time) by make-docs.js

# oc.template.rockylinux.8
## from
 inherit [abcdesktopio/oc.template.rockylinux.minimal.8](../oc.template.rockylinux.minimal.8)

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



> file oc.template.rockylinux.8.md is created at Sat Nov 30 2024 22:38:32 GMT+0000 (Coordinated Universal Time) by make-docs.js

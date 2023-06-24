# oc.template.alpine.gtk
## from
 inherite [abcdesktopio/oc.template.alpine](../oc.template.alpine)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.18.2
PRETTY_NAME="Alpine Linux v3.18"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"

```



## `DockerFile` source code

``` 

# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

# add mesa-dri
# add adwaita theme
RUN apk add --no-cache --update \
        mesa-dri-gallium \
        adwaita-icon-theme \
        libadwaita

```


> file oc.template.alpine.gtk.md is created at Fri Jun 23 2023 16:35:23 GMT+0000 (Coordinated Universal Time) by make-docs.js

``` 

# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

# add mesa-dri
# add adwaita theme
RUN apk add --no-cache --update \
        mesa-dri-gallium \
        adwaita-icon-theme \
        libadwaita

```


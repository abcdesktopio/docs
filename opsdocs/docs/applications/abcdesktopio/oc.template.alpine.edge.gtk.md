# oc.template.alpine.edge.gtk
## from
 inherit [abcdesktopio/oc.template.alpine.edge](../oc.template.alpine.edge)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.20.0_alpha20240315
PRETTY_NAME="Alpine Linux edge"
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



> file oc.template.alpine.edge.gtk.md is created at Wed Mar 27 2024 20:47:55 GMT+0000 (Coordinated Universal Time) by make-docs.js

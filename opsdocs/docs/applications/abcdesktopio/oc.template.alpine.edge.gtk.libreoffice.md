# oc.template.alpine.edge.gtk.libreoffice
## from
 inherit [abcdesktopio/oc.template.alpine.edge.gtk](../oc.template.alpine.edge.gtk)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.18_alpha20230329
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


# add libreoffice
RUN apk add --no-cache --update  \
   faenza-icon-theme-libreoffice \
   libreoffice 			 \
   libreoffice-gtk

```



> file oc.template.alpine.edge.gtk.libreoffice.md is created at Sat Jun 24 2023 08:35:20 GMT+0000 (Coordinated Universal Time) by make-docs.js

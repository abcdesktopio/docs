# oc.template.alpine.edge
## from
 inherit [abcdesktopio/oc.template.alpine.minimal.edge](../oc.template.alpine.minimal.edge)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.20.0_alpha20240329
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


# add some fonts
RUN apk add  --no-cache --update  \
	font-opensans \
	font-adobe-100dpi \
	font-noto 	\
	font-ubuntu-nerd \
	font-dejavu-sans-mono-nerd \
	font-adobe-utopia-100dpi \
	font-xfree86-type1 \
	ttf-freefont \
	font-ibm-type1 \
	font-liberation \
	font-sony-misc

```



> file oc.template.alpine.edge.md is created at Sun May 05 2024 13:45:19 GMT+0000 (Coordinated Universal Time) by make-docs.js

# oc.template.alpine.edge
## from
 inherit [abcdesktopio/oc.template.alpine.minimal.edge](../oc.template.alpine.minimal.edge)

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



> file oc.template.alpine.edge.md is created at Sat Nov 30 2024 22:37:13 GMT+0000 (Coordinated Universal Time) by make-docs.js

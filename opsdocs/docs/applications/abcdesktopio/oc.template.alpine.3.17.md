# oc.template.alpine.3.17
## from
 inherite [abcdesktopio/oc.template.alpine.minimal.3.17](../oc.template.alpine.minimal.3.17)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.17.4
PRETTY_NAME="Alpine Linux v3.17"
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


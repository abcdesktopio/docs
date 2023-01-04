# oc.template.alpine.wine
## from
 inherite [abcdesktopio/oc.template.alpine.minimal](../oc.template.alpine.minimal)
## Container distribution release


``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.17.0
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
	wine

```


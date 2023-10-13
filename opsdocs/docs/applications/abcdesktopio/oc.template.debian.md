# oc.template.debian
## from
 inherit [abcdesktopio/oc.template.debian.minimal](../oc.template.debian.minimal)
## Container distribution release


``` 
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"

```



## `DockerFile` source code

``` 
# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

RUN apt-get update && apt-get install -y --no-install-recommends \
     openssl				\
     sudo				\
     krb5-user 				\
     && apt-get clean			\
     && rm -rf /var/lib/apt/lists/	

```



> file oc.template.debian.md is created at Fri Oct 13 2023 16:19:00 GMT+0000 (Coordinated Universal Time) by make-docs.js

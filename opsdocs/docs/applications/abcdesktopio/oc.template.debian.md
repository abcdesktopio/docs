# oc.template.debian
## from
 inherite [abcdesktopio/oc.template.debian.minimal](../oc.template.debian.minimal)
## Container distribution release


``` 
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
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


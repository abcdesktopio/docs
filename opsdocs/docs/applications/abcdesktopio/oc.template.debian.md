# oc.template.debian
## from
 inherit [abcdesktopio/oc.template.debian.minimal](../oc.template.debian.minimal)

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



> file oc.template.debian.md is created at Sat Nov 30 2024 22:37:28 GMT+0000 (Coordinated Universal Time) by make-docs.js

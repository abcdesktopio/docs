# oc.template.ubuntu.24.04
## from
 inherit [abcdesktopio/oc.template.ubuntu.minimal.24.04](../oc.template.ubuntu.minimal.24.04)

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



> file oc.template.ubuntu.24.04.md is created at Sat Nov 30 2024 22:38:43 GMT+0000 (Coordinated Universal Time) by make-docs.js

# oc.template.ubuntu.20.04
## from
 inherit [abcdesktopio/oc.template.ubuntu.minimal.20.04](../oc.template.ubuntu.minimal.20.04)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal

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



> file oc.template.ubuntu.20.04.md is created at Thu Mar 28 2024 16:10:40 GMT+0000 (Coordinated Universal Time) by make-docs.js

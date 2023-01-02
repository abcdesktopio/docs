# Requirements

## Prerequisites for abcdesktop setup in release 2.x

* Architecture `x86-64` ( `arm-64` is not yet available)
* 16 GB of free space to store sample applications ( `gimp`, `libreoffice writer`, `libreoffice calc`, `libreoffice math`, `libreoffice impress`, `firefox` ) and core image services

## Release 2.x

* Kubernetes release must be less than 1.24

* You need to install `docker` on each worker node. There is a depend to dockerd in all releases 2.x. Application runs as `docker container` or as `kubernetes pod`. 

* `Pyos` service use access to the `dockerd socket`.


## Supported Architectures

Our images support only architectures `x86-64`. The architectures supported by this image is:

| Architecture | Tag |
| :----: | --- |
| x86-64 | amd64-latest |


### GNU/Linux

The recommended distrubution is [Ubuntu 20.04.5 LTS (Focal Fossa)](https://releases.ubuntu.com/20.04/)


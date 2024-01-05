# Requirements

## Prerequisites for setup abcdesktop

* Architecture `x86-64` ( `arm-64` is not yet available)
* 15 GB of free space to store sample applications ( gimp, libreoffice writer, libreoffice calc, libreoffice math, libreoffice impress, firefox ) and core image services
* a kubernetes cluster ready to run **greater or equal** to 1.24

### Release 3.X [ stable ]
* Kubernetes release **greater or equal** to 1.24
* No depend to dockerd, an application runs as pod or as an [ephermeral container](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
* Support storageClass and persistent volume claims
* Support cloud provider 

## Supported Architectures

Our images support only architectures `x86-64`. The architectures supported by this image is:

| Architecture | Tag |
| :----: | --- |
| x86-64 | amd64-latest |

`arm-64` is in progress.


### GNU/Linux

The recommended distrubution is `Ubuntu 22.04.2 LTS`

### MacOS/X

Use Docker Desktop with kubernetes, https://www.docker.com/products/docker-desktop/

### Microsoft Windows

Use Docker Desktop with kubernetes, https://www.docker.com/products/docker-desktop/


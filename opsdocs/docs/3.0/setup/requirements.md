# Requirements

## Prerequisites for abcdesktop setup in release 3.x

* Architecture `x86-64` ( `arm-64` is not yet available)
* 16 GB of free space to store sample applications ( `gimp`, `libreoffice writer`, `libreoffice calc`, `libreoffice math`, `libreoffice impress`, `firefox` ) and core image services

## Release 3.x

* kubernetes release must be greater or equal to 1.24

```
kubectl version --output=yaml
```

```
serverVersion:
  buildDate: "2022-05-24T12:18:48Z"
  compiler: gc
  gitCommit: 3ddd0f45aa91e2f30c70734b175631bec5b5825a
  gitTreeState: clean
  gitVersion: v1.24.1
  goVersion: go1.18.2
  major: "1"
  minor: "24"
  platform: linux/amd64
```

* You do not need to install dockerd. 
* There is no depend to dockerd anymore. In this release and all next releases, application can run as : 
  - `kubernetes pod` 
  - `ephermeral container`. Read more informations about on [`ephermeral container`](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
* All [container-runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) are supported. [containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md) is recommended py default.

## minikube support

[minikube](https://github.com/kubernetes/minikube) is supported in release 3.0. The reverse proxy service need to enable dns service.

- to enable `kube-dns` add one to `minikube`

```
$ minikube start
$ minikube addons enable kube-dns
```

## Supported Architectures

Our images support only architectures `x86-64`. The architectures supported by this image is:

| Architecture | Tag |
| :----: | --- |
| x86-64 | amd64-latest |


### GNU/Linux

The recommended distrubution is [Ubuntu 22.04.1 LTS (Jammy Jellyfish)](https://releases.ubuntu.com/22.04/)


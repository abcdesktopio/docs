# Requirements

## Prerequisites for abcdesktop setup in release 3.x

* Architecture `x86-64` (`arm-64` is not yet available)
* 16 GB of free space to store sample applications (`gimp`, `libreoffice writer`, `libreoffice calc`, `libreoffice math`, `libreoffice impress`, `firefox`) and core image services.

## Release 3.x

* kubernetes release must be greater or equal to 1.24

``` bash
$ kubectl version --output=yaml
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
  - `ephemeral container`. Read more informations about on [`ephermeral container`](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
* All [container-runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) are supported. [containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md) is recommended py default.

## microk8s support

[microk8s](https://microk8s.io/) is supported in abcdesktop release 3.0. The reverse proxy service need to enable dns service.

### microk8s kubectl version

* kubernetes release must be greater or equal to 1.24

``` bash
$ microk8s kubectl version --output=yaml
clientVersion:
  buildDate: "2022-09-28T14:42:45Z"
  compiler: gc
  gitCommit: 949b88ddc8b8cc540684c90c176f92ac9676e07c
  gitTreeState: clean
  gitVersion: v1.24.6-2+949b88ddc8b8cc
  goVersion: go1.18.5
  major: "1"
  minor: 24+
  platform: linux/amd64
kustomizeVersion: v4.5.4
serverVersion:
  buildDate: "2022-09-28T14:40:13Z"
  compiler: gc
  gitCommit: 949b88ddc8b8cc540684c90c176f92ac9676e07c
  gitTreeState: clean
  gitVersion: v1.24.6-2+949b88ddc8b8cc
  goVersion: go1.18.5
  major: "1"
  minor: 24+
  platform: linux/amd64
```

### enable `dns` add one to `microk8s`

``` bash
$ microk8s enable dns
```

You should ready on stdout

``` bash
$ microk8s enable dns
Infer repository core for addon dns
Enabling DNS
Applying manifest
serviceaccount/coredns created
configmap/coredns created
deployment.apps/coredns created
service/kube-dns created
clusterrole.rbac.authorization.k8s.io/coredns created
clusterrolebinding.rbac.authorization.k8s.io/coredns created
Restarting kubelet
DNS is enabled
```

Check microk8s status

``` bash
$ microk8s status
microk8s is running
high-availability: no
  datastore master nodes: 127.0.0.1:19001
  datastore standby nodes: none
addons:
  enabled:
    dns                  # (core) CoreDNS
    ha-cluster           # (core) Configure high availability on the current node
```

## Supported Architectures

images support only architectures `x86-64`. The architectures supported by this image is:

| Architecture | Tag          |
|--------------|--------------|
| x86-64       | amd64-latest |


### GNU/Linux

The recommended distribution is [Ubuntu 22.04.1 LTS (Jammy Jellyfish)](https://releases.ubuntu.com/22.04/)


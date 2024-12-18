# abcdesktop release 3.0

The abcdesktop release 3.0 has started in May 2022

* Kubernetes release **greater or equal** to 1.24
* No depend to docker, an application runs as pod or as an [ephermeral container](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
* All container-runtimes are supported. `containerd` is recommended by default
* abcdesktop release 3.x is unstable, API endpoints can change.

## Architecture abcdesktop 3.0

In release 3.0, the abcdesktop control plane uses only `Kubernetes` API. It doesn't depend to `dockerd`. 

![abcdesktop design](config/img/kubernetes.abcdesktop.3.0.svg)


## Auth service

Auth service supports LDAP Posix Account

## User pod

## Applications

Application can run as : 

  - `kubernetes pod`
  - `kubernetes ephemeral container`

 

### Volumes

#### User's home directories

Define volumes to retain user's home directory files. User's home directory can be mounted as `hostPath` on each worker node or as `persistentVolumeClaim`.
Get more informations about the [persistentVolume and persistentVolumeClaim](config/volumes.md) to retain user datas.







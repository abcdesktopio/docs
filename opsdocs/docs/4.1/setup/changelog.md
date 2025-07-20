# Change log from 4.0 to 4.1


The prominent changes for this release are:

* Fix security issues
* Replace `FROM ubuntu` by `FROM alpine` for core components like `pyos`, `openldap`, `memcache`, `nginx`, and `mongodb`  
* Add support from external auth provider in od.config (and only from od.config file)
* Support `kind: Role` to define `rbac.authorization.k8s.io` if pyos has more than `replicats: 1`. Remove `kind: ClusterRole` to reduce `pyos-serviceaccount` roles.
* `arm64` and `amd64` for all images - including applications and alpine image based

## oc.user images

There is 3 oc.user images, all images are based on `ubuntu:24.04` 

- `ghcr.io/abcdesktopio/oc.user.ubuntu.24.04:4.1` is the default oc.user image with console `webshell` support 
- `ghcr.io/abcdesktopio/oc.user.ubuntu.sudo.24.04:4.1` like oc.user image with `sudo` command embedded, a user can run sudo command inside the container
- `ghcr.io/abcdesktopio/oc.user.hardening.24.04:4.1` less built-in binary, without `sudo` command and without `webshell` console and `terminal` application

All images embedded the graphical services: X11 server (TigerVNC), websockify and plasmashell.











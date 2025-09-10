# Change log from 4.1 to 4.2


The prominent changes for this release are:

* Read Kubernetes events when creating new pod or ephemeral container applications
* Add snapshot features (beta)
* add themes changes (beta)
* Refactoring console application with react.js
* Login page is rendered from `od.config` file, (no need to write css file for a new provider)  
* `arm64` and `amd64` for all images - including applications and alpine image based

## oc.user images

There is 3 oc.user images, all images are based on `ubuntu:24.04` 

- `ghcr.io/abcdesktopio/oc.user.ubuntu.24.04:4.2` is the default oc.user image with console `webshell` support 
- `ghcr.io/abcdesktopio/oc.user.ubuntu.sudo.24.04:4.2` like oc.user image with `sudo` command embedded, a user can run sudo command inside the container
- `ghcr.io/abcdesktopio/oc.user.hardening.24.04:4.2` less built-in binary, without `sudo` command and without `webshell` console and `terminal` application

All images embedded the graphical services: X11 server (TigerVNC), websockify and plasmashell.











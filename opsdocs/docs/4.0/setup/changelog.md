# Change log


The prominent changes for this release are:

* The native KDE Plasma inteface with [Win11OS](https://github.com/yeyushengfan258/Win11OS-kde) theme. KDE Plasmashell application replaces the HTML dock and search text area. 
* Supports hardware accelerated OpenGL and Vulkan on drivers that supports GBM (FOSS drivers and newer Nvidia drivers) with [TigerVNC](https://github.com/TigerVNC/) 1.15.0
* The registry is hosted by gitHub container registry ghcr.io. All images start this this prefix ```ghcr.io/abcdesktopio```. The [abcdesktop.yaml](https://github.com/abcdesktopio/conf/blob/main/kubernetes/abcdesktop-4.0.yaml) yaml file and [od.config](https://github.com/abcdesktopio/conf/blob/main/reference/od.config.4.0) are updated with the prefix.
* [abcdesktop.yaml](https://github.com/abcdesktopio/conf/blob/main/kubernetes/abcdesktop-4.0.yaml) file include ConfigMap to customize user's local account files [ '/etc/passwd', '/etc/group', '/etc/shadow', '/etc/gshadow' ]
* [network policies](https://github.com/abcdesktopio/conf/blob/main/kubernetes/netpol-default-4.0.yaml) support Pod application
* [oc.user](https://raw.githubusercontent.com/abcdesktopio/oc.user/refs/heads/4.0/Dockerfile.ubuntu) image uses ```ubuntu:24.04``` as based image.

## oc.user images

There is 3 oc.user images, all images are based on `ubuntu:24.04` 

- `ghcr.io/abcdesktopio/oc.user.ubuntu.24.04:4.0` is the default oc.user image with console `webshell` support 
- `ghcr.io/abcdesktopio/oc.user.ubuntu.sudo.24.04:4.0` like oc.user image with `sudo` command embedded, a user can run sudo command inside the container
- `ghcr.io/abcdesktopio/oc.user.hardening.24.04:4.0` less built-in binary, without `sudo` command and without `webshell` console and `terminal` application

All images embedded the graphical services: X11 server (TigerVNC), websockify and plasmashell.


## default `balloon` account is deleted

The default `balloon` account does exist anymore, by default. 
The files ( /etc/passwd, /etc/group, /etc/shadow, /etc/gshadow ) are customized during the login process, with the posix user login.
`balloon` account can still be present only if your ldap (or your auth provider) doesn't provide posix groups and account. 

## Compatibily support

The abcdesktop applications in format `3.X` (including 3.4) are compatible with abcdesktop application in format `4.0`.

The `4.0` format includes a change for the files `/etc/shadow` and `/etc/gshadow`.

- /etc/shadow  -> /etc/localaccount.shadow/shadow
- /etc/gshadow -> /etc/localaccount.shadow/gshadow

The symbolic links are linked to the `/etc/localaccount.shadow` volume. Some commands or programs (e.g., su, passwd, adduser and others) access to the shadow file.

If your application need an access to the file '/etc/shadow' or the file '/etc/gshadow', then you have to add this line to your Dockerfile.

```
RUN for f in shadow gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /etc/localaccount.shadow; rm -f /etc/$f; ln -s /etc/localaccount.shadow/$f /etc/$f; fi; done
```

The complete lines for a users support with ( passwd, group ) and ( shadow, gshadow ) 

```
# Create links for local acccounts
# /etc/passwd  -> /etc/localaccount/passwd
# /etc/group   -> /etc/localaccount/group
# /etc/shadow  -> /etc/localaccount.shadow/shadow
# /etc/gshadow -> /etc/localaccount.shadow/gshadow
RUN mkdir -p /etc/localaccount /etc/localaccount.shadow
RUN for f in passwd group ; do if [ -f /etc/$f ] ; then  cp /etc/$f /etc/localaccount; rm -f /etc/$f; ln -s /etc/localaccount/$f /etc/$f; fi; done
RUN for f in shadow gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /etc/localaccount.shadow; rm -f /etc/$f; ln -s /etc/localaccount.shadow/$f /etc/$f; fi; done
```



## abcdesktop.yaml 

Remove the fixed namespace `namespace: abcdesktop` value in `abcdesktop.yaml` 
The namespace value is set using `--namespace` option

```
kubectl apply --namespace abcdesktop -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-4.0.yaml
```












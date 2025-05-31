# Change log


The prominent changes for this release are:

* The native KDE Plasma inteface with [Win11OS](https://github.com/yeyushengfan258/Win11OS-kde) theme. KDE Plasmashell application replaces the HTML dock and search text area. 
* Supports hardware accelerated OpenGL and Vulkan on drivers that supports GBM (FOSS drivers and newer Nvidia drivers) with [TigerVNC](https://github.com/TigerVNC/) 1.15.0
* [abcdesktop.yaml](https://github.com/abcdesktopio/conf/blob/main/kubernetes/abcdesktop-4.0.yaml) file include ConfigMap to customize user's local account files [ '/etc/passwd', '/etc/group', '/etc/shadow', '/etc/gshadow' ]. change file permissions to [ '/etc/shadow', '/etc/gshadow' ]
* [network policies](https://github.com/abcdesktopio/conf/blob/main/kubernetes/netpol-default-4.0.yaml) support Pod application



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






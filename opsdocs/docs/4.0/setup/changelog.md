# Change log


The prominent changes for this release are:

* The native KDE Plasma inteface with [Win11OS](https://github.com/yeyushengfan258/Win11OS-kde) theme. This change removes the HTML dock and search text area. 
* Supports hardware accelerated OpenGL and Vulkan on drivers that supports GBM (FOSS drivers and newer Nvidia drivers) with [TigerVNC](https://github.com/TigerVNC/) 1.15.0
* [abcdesktop.yaml](https://github.com/abcdesktopio/conf/blob/main/kubernetes/abcdesktop-4.0.yaml) file include ConfigMap to customize user's local account files [ '/etc/passwd', '/etc/group', '/etc/shadow', '/etc/gshadow' ]. change file permissions to [ '/etc/shadow', '/etc/gshadow' ]
* [network policies](https://github.com/abcdesktopio/conf/blob/main/kubernetes/netpol-default-4.0.yaml) support Pod application



## Compatibily support

3.4 abcdesktop application format are compatible with 4.0 abcdesktop application.

From oc.user.4.0 Dockerfile 

```
# change passwd shadow group gshadow files
# create a symlink for each files
# target are provisioned in dedicated volumes to support ReadOnly, 
# we can't update files /etc/passwd /etc/group /etc/shadow /etc/gshadow 
# Note: SubPath is not supported in ephemeral 
containers
# Default value :
# ABCDESKTOP_LOCALACCOUNT_DIR = /etc/localaccount

RUN mkdir -p ${ABCDESKTOP_LOCALACCOUNT_DIR} ${ABCDESKTOP_LOCALACCOUNT_DIR}.shadow && \
    for f in passwd group ; do \
	cp /etc/${f} ${ABCDESKTOP_LOCALACCOUNT_DIR} ; \
	rm -f /etc/${f}; \
        ln -s ${ABCDESKTOP_LOCALACCOUNT_DIR}/${f} /etc/${f}; \
    done && \
    for f in shadow gshadow ; do \
        cp /etc/${f} ${ABCDESKTOP_LOCALACCOUNT_DIR}.shadow ; \
        rm -f /etc/${f}; \
        ln -s ${ABCDESKTOP_LOCALACCOUNT_DIR}.shadow/${f} /etc/${f}; \
    done
```

If your application need a access to file '/etc/shadow' or '/etc/gshadow', you have to add this line to your Dockerfile 

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






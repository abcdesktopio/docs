# Change log


The prominent changes for this release are:

* The native KDE Plasma inteface with [Win11OS](https://github.com/yeyushengfan258/Win11OS-kde) theme. This change removes the HTML dock and search text area. 
* Supports hardware accelerated OpenGL and Vulkan on drivers that supports GBM (FOSS drivers and newer Nvidia drivers) with [TigerVNC](https://github.com/TigerVNC/) 1.15.0
* [abcdesktop.yaml](https://github.com/abcdesktopio/conf/blob/main/kubernetes/abcdesktop-4.0.yaml) file include ConfigMap to customize user's local account files [ '/etc/passwd', '/etc/group', '/etc/shadow', '/etc/gshadow' ]. change file permissions to [ '/etc/shadow', '/etc/gshadow' ]
* [network policies](https://github.com/abcdesktopio/conf/blob/main/kubernetes/netpol-default-4.0.yaml) support Pod application
---
title: abcdesktop.io cloud native desktop
summary: cloud container desktop
description: cloud native desktop complete workspace environment accessible from a web browser
keywords: docker kubernetes desktop container cloud native telecommuting remove virtual on demand vdi vnc digital workspace reduce attack surface
---

# Welcome to abcdesktop.io 

abcdesktop.io is a native cloud desktop, and a complete work environment accessible from a simple HTML 5 web browser, without any installation.  Each user’s application runs as a docker container to reduce attack surface.
abcdeskop.io is an opensource free solution that offer secure desktops and applications on any device, network or digital workspace, follow the [https://github.com/abcdesktopio](https://github.com/abcdesktopio) links.


This flexible working environment simplify usage like :

- Telecommuting
- Remote virtual desktop 
- IT temporary access for subcontractors
- Training  
- On demand Desktop


## abcdesktop.io: a docker VDI service

abcdesktop.io provides a way to run grapicals applications securely isolated in a docker container, and use a web browser HTML5 as display device. Because docker containers are lightweight and run without the extra load of an operating system, you can run many graphical applications on a single kernel or even on a kubernetes cluster.

![screenshot-applications](img/screenshot-applications.png)


## Quick installation for kubernetes
You can watch the youtube video sample. This video describes the Quick installation process.

<iframe width="640" height="480" src="https://www.youtube.com/embed/KpjG4ksoGNI" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe>

Download and extract the latest release automatically (Linux or macOS) or read the step by step installation process [abcdesktop for kubernetes](/setup/kubernetes_abcdesktop/)

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install.sh | sh -
```

## Quick installation for docker (personal use, Non-cluster mode)
You can watch the youtube video sample. This video describes the Quick installation process.

<iframe width="640" height="480" src="https://www.youtube.com/embed/_A80Sy9g28I" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe>

Download and extract the latest release automatically (Linux or macOS) or read the step by step installation process [abcdesktop for docker](/setup/dockermode/)

```
curl -L https://raw.githubusercontent.com/abcdesktopio/conf/main/docker/install.sh | sh -
```

## Features

- Complete native cloud desktop, workspace environment
- Authentification OAuth 2.0, LDAP, LDAPS, Active Directory, Kerberos
- Access to the user home directory (homeDirectory support in Active Directory)
- Legacy CIFS Flexvolume using kubernetes driver 
- All applications run inside an isolated docker container
- Local and remote printing support 
- Off-line sessions are maintained
- No need to install applications any more
- Application update, run latest docker image
- Accounting and reporting 

### Applications

- Native support GNU/Linux console native support
- Native support GNU/Linux X11 applications native support
- Support Microsoft Windows applications using wine

### Supported web browser HTML

abcdesktop.io uses many modern web technologies. However these are the minimum versions we are currently aware of:

* Chrome 49, 
* Firefox 58, 
* Safari 11, 
* Opera 36,  
* Microsoft Edge (based on Chromium)

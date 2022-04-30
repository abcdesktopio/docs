# Requirements

## Prerequisites for setup abcdesktop

* Architecture `x86-64`
* A **docker** instance (version 18 and above). You can run docker commands
* 15 GB of free space to store sample applications ( gimp, libreoffice writer, libreoffice calc, libreoffice math, libreoffice impress, firefox ) and core image services


## Supported Architectures

Our images support only architectures `x86-64`. The architectures supported by this image is:

| Architecture | Tag |
| :----: | --- |
| x86-64 | amd64-latest |


## Docker engine

abcdesktop.io uses docker. Docker can run on your desktop, or on a remote server. We recommend to use docker on GNU/Linux for production. To install your specific Docker Engine. Read the [Get started guide](https://docs.docker.com/get-started/) guide from docker.

abcdesktop.io need Docker Engine version 18 and above.


| Operating System | Recommended version                 |
|------------------|-------------------------------------|
|  `GNU/Linux`     | Ubuntu 18.04.4 LTS (Bionic Beaver)  |
|  `macOS/X`       | Catalina version 10.15.3 (and above)| 
|  `Windows 10`    | Version 1703 (and above)            |


### GNU/Linux

The recommended distrubution is [Ubuntu 20.04 LTS (Focal Fossa)](https://releases.ubuntu.com/20.04/)

#### CentOS
To install dockerd on CentOS. Read the docker 'Get Docker Engine' documentation for this Linux distribution.
[Get Docker Engine - Community for CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)

#### Fedora
To install dockerd on Fedora. Read the docker 'Get Docker Engine' documentation for this Linux distribution.
[Get Docker Engine - Community for Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)

#### Debian
To install dockerd on Debian. Read the docker 'Get Docker Engine' documentation for this Linux distribution.
[Get Docker Engine - Community for Debian](https://docs.docker.com/install/linux/docker-ce/debian/)

#### Ubuntu
To install dockerd on Ubuntu. Read the docker 'Get Docker Engine' documentation for this Linux distribution.
[Get Docker Engine - Community for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

#### Binaries
If you want to try Docker or use it in a testing environment, but you’re not on a supported platform, you can try installing from static binaries. If possible, you should use packages built for your operating system, and use your operating system’s package management system to manage Docker installation and upgrades. Be aware that 32-bit static binary archives do not include the Docker daemon.

To install dockerd as binary. Read the docker 'Get Docker Engine' documentation for this Linux distribution.
[Install Docker Engine - Community from binaries](https://docs.docker.com/install/linux/docker-ce/binaries/)


### MacOS/X

Docker For Mac embeds a hypervisor (based on [xhyve](https://github.com/machyve/xhyve)), a Linux distribution which runs on LinuxKit and filesystem & network sharing that is much more Mac native. Docker For Mac is a Mac native application in /Applications. 

At installation time, it creates symlinks in /usr/local/bin for docker and docker-compose, to the commands in the application bundle, in /Applications/Docker.app/Contents/Resources/bin.

To install dockerd on MacOS/X, use Docker for Desktop. Get Docker for MacOS on the docker website 
[docker-for-mac](https://docs.docker.com/docker-for-mac/)

To get a shell to the `LinuxKit docker-desktop`, run the docker command 

```
docker run -it --rm --privileged --pid=host justincormack/nsenter1
```


> more info: [https://github.com/justincormack/nsenter1](https://github.com/justincormack/nsenter1)



### Microsoft Windows

When you install Docker Desktop on Windows, it requires and automatically enables Hyper-V, a hypervisor from Microsoft. Hyper-V replaces your Windows OS as the host on the computer, and your Windows OS becomes a virtual machine. 

####System Requirements
* Windows 10 64-bit: Pro, Enterprise, or Education (Build 15063 or later).
* Hyper-V and Containers Windows features must be enabled.
* 64 bit processor with Second Level Address Translation (SLAT)
* 4GB system RAM
* BIOS-level hardware virtualization support must be enabled in the BIOS settings.


To install dockerd on Microsoft windows, use Docker for Desktop. Get Docker for Windows on the docker website 
[docker-for-windows](https://docs.docker.com/docker-for-windows/)

You need to configure your Docker Desktop on Windows to use **Linux containers**. 
abcdesktop.io **does NOT support Windows container**. 

You can switch the Docker Desktop on Windows to use Linux containers, using  the docker window tray icon. [Switch to Linux containers](/img/switchtolinuxcontainer.png)




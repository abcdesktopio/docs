# Requirements

## Prerequisites for setup abcdesktop

* Architecture `x86-64` ( `arm-64` is not yet available)
* 15 GB of free space to store sample applications ( gimp, libreoffice writer, libreoffice calc, libreoffice math, libreoffice impress, firefox ) and core image services
* a kubernetes cluster ready to run **greater or equal** to 1.24

### Release 3.0 [ stable ]
* Kubernetes release **greater or equal** to 1.24
* No depend to dockerd, an application runs as pod or as an [ephermeral container](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
* Support storageClass and persistent volume claims
* Support cloud provider 

## Supported Architectures

Our images support only architectures `x86-64`. The architectures supported by this image is:

| Architecture | Tag |
| :----: | --- |
| x86-64 | amd64-latest |

`arm-64` is in progress.


### GNU/Linux

The recommended distrubution is `Ubuntu 22.04.2 LTS`

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




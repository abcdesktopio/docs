# oc.template.ubuntu.wine.mswindow
## from
 inherit [abcdesktopio/oc.template.ubuntu.wine](../oc.template.ubuntu.wine)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal

```



## `DockerFile` source code

``` 
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG} 

ENV DEBIAN_FRONTEND noninteractive 
RUN apt-get update && \
 	apt-get install --install-recommends -y \
	xterm \
	wget \
	netcat \
	file \
	winbind \
	gettext \ 
	libgettextpo-dev \
	&& rm -rf /var/lib/apt/lists/*	

# set arch to i386
RUN dpkg --add-architecture i386

# install play
RUN apt-get update && apt-get install -y --no-install-recommends \
	libosmesa6:i386	\
        libnss-mdns \
	libnss-mdns:i386 \
	libncurses5:i386 \
	libodbc1:i386 \
	libxext6:i386 \
	libxi6:i386 \
	libfreetype6:i386 \
	libx11-6:i386 \
	libz1:i386 \
	libcups2:i386 \
	liblcms2-2:i386 \
	libglu1-mesa:i386 \
	libxcursor1:i386 \
	libxrandr2:i386 \
	libxml2:i386 \
	libgl1-mesa-dri:i386 \
	libgl1-mesa-glx:i386 \
	&& rm -rf /var/lib/apt/lists/*

# add source play on linux 
RUN apt-get update && \
   wget https://www.playonlinux.com/script_files/PlayOnLinux/4.3.4/PlayOnLinux_4.3.4.deb && \
   apt-get install --allow-downgrades -y ./PlayOnLinux_4.3.4.deb && \
   rm PlayOnLinux_4.3.4.deb && \
   rm -rf /var/lib/apt/lists/*

```



> file oc.template.ubuntu.wine.mswindow.md is created at Wed Jan 31 2024 14:08:19 GMT+0000 (Coordinated Universal Time) by make-docs.js

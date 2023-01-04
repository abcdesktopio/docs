# oc.template.ubuntu.wine.mswindow
## from
 inherite [abcdesktopio/oc.template.ubuntu.wine.22.04](../oc.template.ubuntu.wine.22.04)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="20.04.1 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.1 LTS"
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
FROM abcdesktopio/oc.template.gtk.wine:$TAG
ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update && \
 	apt-get install --install-recommends -y \
	xterm			\
	wget			\
	netcat			\
	file			\
	winbind			\
	gettext			\ 
	libgettextpo-dev 	\
	python-dbus 		\
	&& rm -rf /var/lib/apt/lists/*	

# add source play on linux 
RUN wget -q "http://deb.playonlinux.com/public.gpg" -O- | sudo apt-key add -
RUN wget http://deb.playonlinux.com/playonlinux_bionic.list -O /etc/apt/sources.list.d/playonlinux.list
# install play
RUN apt-get update && apt-get install -y --no-install-recommends	\
        playonlinux					\
	libosmesa6:i386					\
        libnss-mdns					\
	libnss-mdns:i386				\
	libncurses5:i386				\
	libodbc1:i386					\
	libxext6:i386 					\
	libxi6:i386 					\
	libfreetype6:i386  				\
	libx11-6:i386 					\
	libz1:i386 					\
	libcups2:i386 					\
	liblcms2-2:i386 				\
	libglu1-mesa:i386 				\
	libxcursor1:i386 				\
	libxrandr2:i386 				\
	libxml2:i386					\
	libgl1-mesa-dri:i386 				\
	libgl1-mesa-glx:i386				\
	&& rm -rf /var/lib/apt/lists/*


```


# oc.template.ubuntu.gtk.libreoffice
## from
 inherite [abcdesktopio/oc.template.ubuntu.gtk.20.04](../oc.template.ubuntu.gtk.20.04)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="20.04.5 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.5 LTS"
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
# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:${TAG}

ENV DEBIAN_FRONTEND noninteractive

# install help in all language
#RUN DEBIAN_FRONTEND=noninteractive  apt-get update && apt-get install -y  --no-install-recommends       \
#        $(apt-cache search language-pack-gnome | awk '{print $1 }')                \
#        && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt install -y  			 	\
	at-spi2-core						\
    	libreoffice 						\
	libreoffice-gtk3					\
	libreoffice-style-elementary 				\
	libreoffice-base-drivers				\
	libreoffice-sdbc-hsqldb					\
 	libghc-hdbc-dev						\	
 	&& apt-get clean

# install help in all language
#RUN apt-get update && apt-get install -y  --no-install-recommends	\
#	$(apt-cache search libreoffice-help | awk '{print $1 }')	\
#	&& apt-get clean

# install myspell-dictionary packages when available
#RUN DEBIAN_FRONTEND=noninteractive  apt-get update && apt-get install -y	\       
#        $(apt-cache search myspell-dictionary | awk '{print $1 }')		\
#       && rm -rf /var/lib/apt/lists/*

# install hyphen when available
#RUN apt-get update && apt-get install -y --no-install-recommends       	\       
#        $(apt-cache search hyphen | awk '{print $1 }')                	\
#    && apt-get clean


# install ibreoffice-grammarcheck when available
#RUN apt-get update && apt-get install -y  --no-install-recommends       \
#        $(apt-cache search libreoffice-grammarcheck | awk '{print $1 }') \
#    && apt-get clean


# l10n files are loaded by libreoffice-help packages when available
#RUN apt-get update && apt-get install -y  --no-install-recommends 	\
#	$(apt-cache search libreoffice-l10n | awk '{print $1 }')	\
#    && apt-get clean

#
# install xfonts
# install dbus
RUN apt-get update && apt-get install -y --no-install-recommends  	\
        xfonts-base	\
        dbus-x11	\
    && apt-get clean

RUN mkdir -p /run/user/ && chmod 777 /run/user/


```


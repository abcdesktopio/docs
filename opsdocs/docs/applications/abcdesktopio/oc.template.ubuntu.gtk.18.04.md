# oc.template.ubuntu.gtk.18.04
## from
 inherit [abcdesktopio/oc.template.ubuntu.18.04](../oc.template.ubuntu.18.04)
## Container distribution release


``` 
NAME="Ubuntu"
VERSION="18.04.6 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.6 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic

```



## `DockerFile` source code

``` 
# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE=abcdesktopio/oc.template.22.04
FROM ${BASE_IMAGE}:${TAG} 

# install gtk lib
RUN apt-get update && apt-get install -y --no-install-recommends        \
	gir1.2-gtk-3.0				\
	gir1.2-gtkclutter-1.0			\
	gtk2-engines-murrine			\
	gtk2-engines-pixbuf			\
	libclutter-gtk-1.0-0			\
	libcolord-gtk1				\
	libgtk-3-0				\
     && apt-get clean                           \
     && rm -rf /var/lib/apt/lists/*

RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

#
# install fonts
RUN apt-get update && apt-get install -y --no-install-recommends        \
     xfonts-base \
     xfonts-encodings \
     xfonts-scalable \
     xfonts-utils \
     fonts-dejavu-core	\
     fonts-droid-fallback \
     fonts-freefont-ttf	\
     fonts-guru	\
     fonts-guru-extra \
     fonts-liberation \
     fonts-liberation2 \
     fonts-noto \
     fonts-opensymbol \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    curl -Ls https://mirrors.kernel.org/ubuntu/pool/main/u/ubuntu-font-family-sources/ttf-ubuntu-font-family_0.83-0ubuntu2_all.deb -o /tmp/ttf-ubuntu-font-family_0.83-0ubuntu2_all.deb && \
    apt-get install -f /tmp/ttf-ubuntu-font-family_0.83-0ubuntu2_all.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*


# install https://github.com/vinceliuice/Mojave-gtk-theme
#
# install https://github.com/vinceliuice/Mojave-gtk-theme
#

RUN apt-get update && apt-get install -y --no-install-recommends \
	sassc			\
     	optipng			\
	gtk2-engines-murrine	\
	gtk2-engines-pixbuf	\
	gnome-themes-extra 


COPY --from=abcdesktopio/oc.themes /usr/share/icons  /usr/share/icons
COPY --from=abcdesktopio/oc.themes /usr/share/themes /usr/share/themes

```



> file oc.template.ubuntu.gtk.18.04.md is created at Sun Dec 01 2024 11:59:18 GMT+0000 (Coordinated Universal Time) by make-docs.js

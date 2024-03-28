# oc.template.ubuntu.gtk.20.04
## from
 inherit [abcdesktopio/oc.template.ubuntu.20.04](../oc.template.ubuntu.20.04)
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
# default TAG is dev
ARG TAG=dev
ARG BASE_IMAGE=abcdesktopio/oc.template.22.04
FROM ${BASE_IMAGE}:${TAG} 

# install gtk lib
RUN apt-get update && apt-get install -y --no-install-recommends        \
	gir1.2-gtk-3.0				\
	gir1.2-gtkclutter-1.0			\
	gir1.2-javascriptcoregtk-4.0		\
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
     fonts-noto                 \
     xfonts-base		\
     xfonts-encodings		\
     xfonts-scalable		\
     xfonts-utils		\
     fonts-beng			\
     fonts-beng-extra	\
     fonts-dejavu-core	\
     fonts-deva	\
     fonts-deva-extra	\
     fonts-droid-fallback	\
     fonts-freefont-ttf	\
     fonts-gargi	\
     fonts-gubbi	\
     fonts-gujr	\
     fonts-gujr-extra	\
     fonts-guru	\
     fonts-guru-extra	\
     fonts-indic	\
     fonts-kacst	\
     fonts-kacst-one	\
     fonts-kalapi	\
     fonts-knda	\
     fonts-lao	\
     fonts-lato	\
     fonts-liberation	\
     fonts-liberation2	\
     fonts-lklug-sinhala	\
     fonts-lohit-beng-assamese	\
     fonts-lohit-beng-bengali	\
     fonts-lohit-deva	\
     fonts-lohit-gujr	\
     fonts-lohit-guru	\
     fonts-lohit-knda	\
     fonts-lohit-mlym	\
     fonts-lohit-orya	\
     fonts-lohit-taml	\
     fonts-lohit-taml-classical	\
     fonts-lohit-telu	\
     fonts-mlym	\
     fonts-nakula	\
     fonts-navilu	\
     fonts-noto-cjk	\
     fonts-noto-color-emoji	\
     fonts-noto-mono	\
     fonts-opensymbol	\
     fonts-orya	\
     fonts-orya-extra	\
     fonts-pagul	\
     fonts-sahadeva	\
     fonts-samyak-deva	\
     fonts-samyak-gujr	\
     fonts-samyak-mlym	\
     fonts-samyak-taml	\
     fonts-sarai	\
     fonts-sil-abyssinica	\
     fonts-sil-padauk	\
     fonts-smc	\
     fonts-smc-anjalioldlipi	\
     fonts-smc-chilanka	\
     fonts-smc-dyuthi	\
     fonts-smc-karumbi	\
     fonts-smc-keraleeyam	\
     fonts-smc-manjari	\
     fonts-smc-meera	\
     fonts-smc-rachana	\
     fonts-smc-raghumalayalamsans	\
     fonts-smc-suruma	\
     fonts-smc-uroob	\
     fonts-taml	\
     fonts-telu	\
     fonts-telu-extra	\
     fonts-thai-tlwg	\
     fonts-tibetan-machine	\
     fonts-tlwg-garuda	\
     fonts-tlwg-garuda-ttf	\
     fonts-tlwg-kinnari	\
     fonts-tlwg-kinnari-ttf	\
     fonts-tlwg-laksaman	\
     fonts-tlwg-laksaman-ttf	\
     fonts-tlwg-loma	\
     fonts-tlwg-loma-ttf	\
     fonts-tlwg-mono	\
     fonts-tlwg-mono-ttf	\
     fonts-tlwg-norasi	\
     fonts-tlwg-norasi-ttf	\
     fonts-tlwg-purisa	\
     fonts-tlwg-purisa-ttf	\
     fonts-tlwg-sawasdee	\
     fonts-tlwg-sawasdee-ttf	\
     fonts-tlwg-typewriter	\
     fonts-tlwg-typewriter-ttf	\
     fonts-tlwg-typist	\
     fonts-tlwg-typist-ttf	\
     fonts-tlwg-typo	\
     fonts-tlwg-typo-ttf	\
     fonts-tlwg-umpush	\
     fonts-tlwg-umpush-ttf	\
     fonts-tlwg-waree	\
     fonts-tlwg-waree-ttf	\
     fonts-urw-base35	\
     fonts-yrsa-rasa	\
     && apt-get clean                                   \
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



> file oc.template.ubuntu.gtk.20.04.md is created at Thu Mar 28 2024 16:18:29 GMT+0000 (Coordinated Universal Time) by make-docs.js

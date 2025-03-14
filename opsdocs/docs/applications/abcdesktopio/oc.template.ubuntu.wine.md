# oc.template.ubuntu.wine
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
ARG TAG=dev
ARG BASE_IMAGE
FROM ${BASE_IMAGE}:$TAG
MAINTAINER Alexandre DEVELY 

# install wget
RUN apt-get update && apt-get install --no-install-recommends --yes \
       wget                       		\
       && apt-get clean


# set arch to i386
RUN if [ $(dpkg --print-architecture) == 'amd64' ]; then dpkg --add-architecture i386; fi

# only to use wine repo
# RUN wget -qO - https://dl.winehq.org/wine-builds/winehq.key | apt-key add -
# RUN apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main'


# tools for winetricks
# Uses the following non-POSIX system tools:
# - wine is used to execute Win32 apps except on Cygwin.
# - ar, cabextract, unrar, unzip, and 7z are needed by some verbs.
# - aria2c, wget, curl, or fetch is needed for downloading.
# - fuseiso, archivemount (Linux), or hdiutil (macOS) is used to mount .iso images.
# - perl is used to munge steam config files.
# - pkexec, sudo, or kdesu (gksu/gksudo/kdesudo are deprecated upstream but also still supported)
#   are used to mount .iso images if the user cached them with -k option.
# - sha256sum, sha256, or shasum (OSX 10.5 does not support these, 10.6+ is required)
# - torify is used with option "--torify" if sites are blocked in single countries.
# - xdg-open (if present) or open (for OS X) is used to open download pages
#   for the user when downloads cannot be fully automated.
# - xz is used by some verbs to decompress tar archives.
# - zenity is needed by the GUI, though it can limp along somewhat with kdialog/xmessage.


#RUN apt-get update && \
#    apt-get install --no-install-recommends --yes aria2 \
#    apt-get clean 
    
# RUN apt-get update && \
#    apt-get install --no-install-recommends --yes binutils \
#    apt-get clean 
    
# RUN apt-get update && \
#    apt-get install --no-install-recommends --yes cabextract fuseiso p7zip-full policykit-1 && \
#    apt-get clean     

# RUN apt-get update && \
#    apt-get install --no-install-recommends --yes fuseiso && \
#    apt-get clean  
    
# RUN apt-get update && \
#    apt-get install --no-install-recommends --yes  p7zip-full policykit-1 && \
#    apt-get clean  

# RUN apt-get update && \
#     apt-get install --no-install-recommends --yes  policykit-1 && \
#    apt-get clean  

# RUN apt-get update && \
#    apt-get install --no-install-recommends --yes tor unrar unzip xdg-utils xz-utils zenity && \
#    apt-get clean 
 
# gir1.2-gtk-3.0:i386 gir1.2-pango-1.0:i386 used by crossover

# add for 20.04
# apt-get install --no-install-recommends --yes libgcc-s1:i386 && \

# RUN apt-get update && \
#    apt-get install --no-install-recommends --yes aptitude libnss-mdns:i386 libsdl2-2.0-0 libsdl2-2.0-0:i386 gir1.2-gtk-3.0:i386 gir1.2-pango-1.0:i386 && \
#    apt-get clean 

# add dns support for 32 apps running on 64 bits
#RUN apt-get update && apt-get install -y 	\
#	libnss-mdns-i386			\
#	libnss-mdns				\ 
#	wine-stable	&&			\
#	apt-get clean		

# RUN wget https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/amd64/libfaudio0_19.07-0~bionic_amd64.deb 	&&	\
#     dpkg -i libfaudio0_19.07-0~bionic_amd64.deb 											&&	\
#    rm libfaudio0_19.07-0~bionic_amd64.deb
 
#RUN wget https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/xUbuntu_18.04/i386/libfaudio0_19.07-0~bionic_i386.deb	&&	\
#    dpkg -i libfaudio0_19.07-0~bionic_i386.deb												&&	\
#    rm libfaudio0_19.07-0~bionic_i386.deb


###
#RUN mkdir -p /composer/.cache
#RUN mkdir -p /composer/.cache/wine && \
#	wget  -O  /composer/.cache/wine/wine-gecko-2.47.1-x86.msi http://dl.winehq.org/wine/wine-gecko/2.47.1/wine-gecko-2.47.1-x86.msi && \
#	wget  -O  /composer/.cache/wine/wine-gecko-2.47.1-x86_64.msi http://dl.winehq.org/wine/wine-gecko/2.47.1/wine-gecko-2.47.1-x86_64.msi && \
#	wget  -O  /composer/.cache/wine/wine-mono-4.9.4.msi https://dl.winehq.org/wine/wine-mono/4.9.4/wine-mono-4.9.4.msi		
##

RUN mkdir -p /composer/.cache/fontconfig
# COPY composer/.cache/fontconfig /composer/.cache/fontconfig

RUN apt-get update && \
    apt-get install --yes wine && \
    apt-get clean
 
# add xrdb for playonlinux
# xrdb is in x11-xserver-utils
RUN apt-get update && \
    apt-get install --no-install-recommends --yes libpython3.6 playonlinux x11-xserver-utils && \
    apt-get clean


RUN apt-get update && \
    apt-get install --no-install-recommends --yes mono-runtime winetricks && \
    apt-get clean

COPY composer/updatereg.py              /composer
COPY composer/init.d/init.wine		/composer/init.d/init.wine
COPY composer/init.d/_init.wine         /composer/init.d/_init.wine
RUN  mkdir /composer/.wine /composer/bin && chmod 777 /composer/.wine /composer/bin

# Set for each app 
ENV WINEPREFIX=/composer/.wine
#ENV WINEARCH win32

```



> file oc.template.ubuntu.wine.md is created at Tue Jan 28 2025 14:18:38 GMT+0000 (Coordinated Universal Time) by make-docs.js

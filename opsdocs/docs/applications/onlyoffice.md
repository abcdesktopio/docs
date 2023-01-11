# onlyoffice
![onlyoffice-desktopeditors.svg](icons/onlyoffice-desktopeditors.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](../abcdesktopio/oc.template.ubuntu.gtk)
## Distribution
ubuntu ![ubuntu](icons/ubuntu.svg){: style="height:32px;"}

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


## Ubuntu packages

``` 
onlyoffice-desktopeditors
```

## Licence
 ** This application is NO FREE. ** You need to build it manually.

## Displayname


``` 
OnlyOffice
```

## Path


``` 
/usr/bin/desktopeditors
```

## Mimetype

``` 
application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-template;application/vnd.oasis.opendocument.text-web;application/vnd.oasis.opendocument.text-master;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.template;application/vnd.sun.xml.writer.global;application/msword;application/vnd.ms-word;application/x-doc;application/rtf;text/rtf;application/vnd.wordperfect;application/wordperfect;application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.ms-word.document.macroenabled.12;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/vnd.ms-word.template.macroenabled.12;application/vnd.oasis.opendocument.spreadsheet;application/vnd.oasis.opendocument.spreadsheet-template;application/vnd.sun.xml.calc;application/vnd.sun.xml.calc.template;application/msexcel;application/vnd.ms-excel;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/vnd.ms-excel.sheet.macroenabled.12;application/vnd.openxmlformats-officedocument.spreadsheetml.template;application/vnd.ms-excel.template.macroenabled.12;application/vnd.ms-excel.sheet.binary.macroenabled.12;text/csv;text/spreadsheet;application/csv;application/excel;application/x-excel;application/x-msexcel;application/x-ms-excel;text/comma-separated-values;text/tab-separated-values;text/x-comma-separated-values;text/x-csv;application/vnd.oasis.opendocument.presentation;application/vnd.oasis.opendocument.presentation-template;application/vnd.sun.xml.impress;application/vnd.sun.xml.impress.template;application/mspowerpoint;application/vnd.ms-powerpoint;application/vnd.openxmlformats-officedocument.presentationml.presentation;application/vnd.ms-powerpoint.presentation.macroenabled.12;application/vnd.openxmlformats-officedocument.presentationml.template;application/vnd.ms-powerpoint.template.macroenabled.12;application/vnd.openxmlformats-officedocument.presentationml.slide;application/vnd.openxmlformats-officedocument.presentationml.slideshow;application/vnd.ms-powerpoint.slideshow.macroEnabled.12;
```

## File extensions
`"doc;docx;odt;rtf;txt;xls;xlsx;ods;csv;ppt;pptx;odp"`
## ACL

``` json
{
    "permit": [
        "all"
    ]
}
```

## WM_CLASS

``` 
DesktopEditors.DesktopEditors
```

> The WM_CLASS property (of type STRING without control characters) contains two consecutive null-terminated strings. These specify the Instance and Class names to be used by both the client and the window manager for looking up resources for the application or as identifying information.
> to get the WM_CLASS property of an application, use the command line `wmctrl -lx`

## Desktopfile

``` 
/usr/share/applications/onlyoffice-desktopeditors.desktop
```

> A .desktop file is a simple text file that holds information about a program. It is usually placed in “/usr/share/applications/”.

## PRE run command

> PRE run command are run **before** the package install command

```
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys CB2DE8E5
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
RUN echo "deb [arch=$(dpkg --print-architecture)] https://download.onlyoffice.com/repo/debian squeeze main" > /etc/apt/sources.list.d/onlyoffice.list
RUN apt-get update && apt-get install --yes libgl1 libnss3 qt5dxcb-plugin && apt-get clean && rm -rf /var/lib/apt/lists/*
```



## JSON dump
json source file onlyoffice.d.3.0.json 

``` json
{
    "acl": {
        "permit": [
            "all"
        ]
    },
    "cat": "office",
    "preruncommands": [
        "RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys CB2DE8E5",
        "RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections",
        "RUN echo \"deb [arch=$(dpkg --print-architecture)] https://download.onlyoffice.com/repo/debian squeeze main\" > /etc/apt/sources.list.d/onlyoffice.list",
        "RUN apt-get update && apt-get install --yes libgl1 libnss3 qt5dxcb-plugin && apt-get clean && rm -rf /var/lib/apt/lists/*"
    ],
    "debpackage": "onlyoffice-desktopeditors",
    "icon": "onlyoffice-desktopeditors.svg",
    "installrecommends": true,
    "keyword": "office,onlyoffice,desktop,editor",
    "launch": "DesktopEditors.DesktopEditors",
    "name": "onlyoffice",
    "displayname": "OnlyOffice",
    "rules": {
        "homedir": {
            "default": true
        }
    },
    "path": "/usr/bin/desktopeditors",
    "template": "abcdesktopio/oc.template.ubuntu.gtk",
    "mimetype": "application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-template;application/vnd.oasis.opendocument.text-web;application/vnd.oasis.opendocument.text-master;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.template;application/vnd.sun.xml.writer.global;application/msword;application/vnd.ms-word;application/x-doc;application/rtf;text/rtf;application/vnd.wordperfect;application/wordperfect;application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.ms-word.document.macroenabled.12;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/vnd.ms-word.template.macroenabled.12;application/vnd.oasis.opendocument.spreadsheet;application/vnd.oasis.opendocument.spreadsheet-template;application/vnd.sun.xml.calc;application/vnd.sun.xml.calc.template;application/msexcel;application/vnd.ms-excel;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/vnd.ms-excel.sheet.macroenabled.12;application/vnd.openxmlformats-officedocument.spreadsheetml.template;application/vnd.ms-excel.template.macroenabled.12;application/vnd.ms-excel.sheet.binary.macroenabled.12;text/csv;text/spreadsheet;application/csv;application/excel;application/x-excel;application/x-msexcel;application/x-ms-excel;text/comma-separated-values;text/tab-separated-values;text/x-comma-separated-values;text/x-csv;application/vnd.oasis.opendocument.presentation;application/vnd.oasis.opendocument.presentation-template;application/vnd.sun.xml.impress;application/vnd.sun.xml.impress.template;application/mspowerpoint;application/vnd.ms-powerpoint;application/vnd.openxmlformats-officedocument.presentationml.presentation;application/vnd.ms-powerpoint.presentation.macroenabled.12;application/vnd.openxmlformats-officedocument.presentationml.template;application/vnd.ms-powerpoint.template.macroenabled.12;application/vnd.openxmlformats-officedocument.presentationml.slide;application/vnd.openxmlformats-officedocument.presentationml.slideshow;application/vnd.ms-powerpoint.slideshow.macroEnabled.12;",
    "args": "",
    "fileextensions": "doc;docx;odt;rtf;txt;xls;xlsx;ods;csv;ppt;pptx;odp",
    "desktopfile": "/usr/share/applications/onlyoffice-desktopeditors.desktop",
    "licence": "non-free"
}
```

## Install the builded image
>Replace the **ABCHOST** var set to localhost by default to your own server ip address

``` sh
ABCHOST=localhost
curl --output onlyoffice.d.3.0.json https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/onlyoffice.d.3.0.json
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @onlyoffice.d.3.0.json

```

## Generated `DockerFile` source code

``` 
# Dynamic DockerFile application file for abcdesktopio generated by abcdesktopio/oc.apps/make.js
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
ARG TAG=dev
FROM abcdesktopio/oc.template.ubuntu.gtk:$TAG
USER root
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys CB2DE8E5
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
RUN echo "deb [arch=$(dpkg --print-architecture)] https://download.onlyoffice.com/repo/debian squeeze main" > /etc/apt/sources.list.d/onlyoffice.list
RUN apt-get update && apt-get install --yes libgl1 libnss3 qt5dxcb-plugin && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y onlyoffice-desktopeditors && apt-get clean
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
LABEL oc.icon="onlyoffice-desktopeditors.svg"
LABEL oc.icondata="PHN2ZyB3aWR0aD0iNzIiIGhlaWdodD0iNjciIHZpZXdCb3g9IjAgMCA3MiA2NyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0zMS41MDMzIDY1Ljc3NDJMMS44OTE4NCA1Mi4xODA1Qy0wLjYzMDYxNSA1MC45OTM3IC0wLjYzMDYxNSA0OS4xNTk2IDEuODkxODQgNDguMDgwOEwxMi4yMDEgNDMuMzMzN0wzMS4zOTM2IDUyLjE4MDVDMzMuOTE2MSA1My4zNjcyIDM3Ljk3NCA1My4zNjcyIDQwLjM4NjggNTIuMTgwNUw1OS41Nzk0IDQzLjMzMzdMNjkuODg4NiA0OC4wODA4QzcyLjQxMSA0OS4yNjc1IDcyLjQxMSA1MS4xMDE2IDY5Ljg4ODYgNTIuMTgwNUw0MC4yNzcxIDY1Ljc3NDJDMzcuOTc0IDY2Ljg1MyAzMy45MTYxIDY2Ljg1MyAzMS41MDMzIDY1Ljc3NDJaIiBmaWxsPSJ1cmwoI3BhaW50MF9saW5lYXIpIi8+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMzEuNTAzMyA0OS4wNTE2TDEuODkxODQgMzUuNDU3OEMtMC42MzA2MTUgMzQuMjcxMSAtMC42MzA2MTUgMzIuNDM3IDEuODkxODQgMzEuMzU4MUwxMS45ODE3IDI2LjcxOUwzMS41MDMzIDM1LjY3MzZDMzQuMDI1OCAzNi44NjAzIDM4LjA4MzYgMzYuODYwMyA0MC40OTY0IDM1LjY3MzZMNjAuMDE4MSAyNi43MTlMNzAuMTA3OSAzMS4zNTgxQzcyLjYzMDQgMzIuNTQ0OSA3Mi42MzA0IDM0LjM3OSA3MC4xMDc5IDM1LjQ1NzhMNDAuNDk2NCA0OS4wNTE2QzM3Ljk3NCA1MC4yMzgzIDMzLjkxNjEgNTAuMjM4MyAzMS41MDMzIDQ5LjA1MTZaIiBmaWxsPSJ1cmwoI3BhaW50MV9saW5lYXIpIi8+CjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMzEuNTAzMyAzMi43NjA2TDEuODkxODQgMTkuMTY2OUMtMC42MzA2MTUgMTcuOTgwMSAtMC42MzA2MTUgMTYuMTQ2IDEuODkxODQgMTUuMDY3MkwzMS41MDMzIDEuNDczNDRDMzQuMDI1OCAwLjI4NjY4NSAzOC4wODM2IDAuMjg2Njg1IDQwLjQ5NjQgMS40NzM0NEw3MC4xMDc5IDE1LjA2NzJDNzIuNjMwNCAxNi4yNTM5IDcyLjYzMDQgMTguMDg4IDcwLjEwNzkgMTkuMTY2OUw0MC40OTY0IDMyLjc2MDZDMzcuOTc0IDMzLjgzOTUgMzMuOTE2MSAzMy44Mzk1IDMxLjUwMzMgMzIuNzYwNloiIGZpbGw9InVybCgjcGFpbnQyX2xpbmVhcikiLz4KPGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQwX2xpbmVhciIgeDE9IjM1Ljk3NDMiIHkxPSI3OC42NTk0IiB4Mj0iMzUuOTc0MyIgeTI9IjI5LjAzMDIiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iI0ZDQzJCMSIvPgo8c3RvcCBvZmZzZXQ9IjAuODg0OCIgc3RvcC1jb2xvcj0iI0Q5NDIwQiIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXIiIHgxPSIzNS45NzQzIiB5MT0iNTcuMTcxMyIgeDI9IjM1Ljk3NDMiIHkyPSIyNC41MzE2IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNERUVEQzkiLz4KPHN0b3Agb2Zmc2V0PSIwLjY2MDYiIHN0b3AtY29sb3I9IiM4QkJBMjUiLz4KPC9saW5lYXJHcmFkaWVudD4KPGxpbmVhckdyYWRpZW50IGlkPSJwYWludDJfbGluZWFyIiB4MT0iMzUuOTc0MyIgeTE9IjQzLjk1NDciIHgyPSIzNS45NzQzIiB5Mj0iLTAuNDYwODYyIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNDMkVCRkEiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjMjZBOERFIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+Cg=="
LABEL oc.keyword="onlyoffice,office,onlyoffice,desktop,editor"
LABEL oc.cat="office"
LABEL oc.desktopfile="onlyoffice-desktopeditors.desktop"
LABEL oc.launch="DesktopEditors.DesktopEditors"
LABEL oc.template="abcdesktopio/oc.template.ubuntu.gtk"
LABEL oc.name="onlyoffice"
LABEL oc.displayname="OnlyOffice"
LABEL oc.path="/usr/bin/desktopeditors"
LABEL oc.type=app
LABEL oc.licence="non-free"
LABEL oc.mimetype="application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-template;application/vnd.oasis.opendocument.text-web;application/vnd.oasis.opendocument.text-master;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.template;application/vnd.sun.xml.writer.global;application/msword;application/vnd.ms-word;application/x-doc;application/rtf;text/rtf;application/vnd.wordperfect;application/wordperfect;application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.ms-word.document.macroenabled.12;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/vnd.ms-word.template.macroenabled.12;application/vnd.oasis.opendocument.spreadsheet;application/vnd.oasis.opendocument.spreadsheet-template;application/vnd.sun.xml.calc;application/vnd.sun.xml.calc.template;application/msexcel;application/vnd.ms-excel;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/vnd.ms-excel.sheet.macroenabled.12;application/vnd.openxmlformats-officedocument.spreadsheetml.template;application/vnd.ms-excel.template.macroenabled.12;application/vnd.ms-excel.sheet.binary.macroenabled.12;text/csv;text/spreadsheet;application/csv;application/excel;application/x-excel;application/x-msexcel;application/x-ms-excel;text/comma-separated-values;text/tab-separated-values;text/x-comma-separated-values;text/x-csv;application/vnd.oasis.opendocument.presentation;application/vnd.oasis.opendocument.presentation-template;application/vnd.sun.xml.impress;application/vnd.sun.xml.impress.template;application/mspowerpoint;application/vnd.ms-powerpoint;application/vnd.openxmlformats-officedocument.presentationml.presentation;application/vnd.ms-powerpoint.presentation.macroenabled.12;application/vnd.openxmlformats-officedocument.presentationml.template;application/vnd.ms-powerpoint.template.macroenabled.12;application/vnd.openxmlformats-officedocument.presentationml.slide;application/vnd.openxmlformats-officedocument.presentationml.slideshow;application/vnd.ms-powerpoint.slideshow.macroEnabled.12;"
LABEL oc.fileextensions="doc;docx;odt;rtf;txt;xls;xlsx;ods;csv;ppt;pptx;odp"
LABEL oc.rules="{\"homedir\":{\"default\":true}}"
LABEL oc.acl="{\"permit\":[\"all\"]}"
RUN for d in /usr/share/icons /usr/share/pixmaps ; do echo "testing link in $d"; if [ -d $d ] && [ -x /composer/safelinks.sh ] ; then echo "fixing link in $d"; cd $d ; /composer/safelinks.sh ; fi; done
ENV APPNAME "onlyoffice"
ENV APPBIN "/usr/bin/desktopeditors"
ENV APP "/usr/bin/desktopeditors"
USER root
RUN mkdir -p /var/secrets/abcdesktop/localaccount
RUN for f in passwd shadow group gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /var/secrets/abcdesktop/localaccount; rm -f /etc/$f; ln -s /var/secrets/abcdesktop/localaccount/$f /etc/$f; fi; done
USER balloon
CMD [ "/composer/appli-docker-entrypoint.sh" ]

```

## Rebuild the image manually

### Download the Dockerfile manually
[Dockerfile for application onlyoffice](https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/onlyoffice.d)
``` sh
wget https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/onlyoffice.d
```

### build the `Dockerfile` to create a container image

``` sh
docker build --build-arg TAG=3.0 -f onlyoffice.d -t onlyoffice .
```

### Install the new image
>If you are using `containerd` as container runtime, use the ctr command line

 
>If you are not running this bash command on your abcdesktop node
>Replace the **ABCHOST** variable set to localhost by default to your own server ip address


``` sh
ABCHOST=localhost
docker inspect onlyoffice > onlyoffice.json
docker image save onlyoffice -o onlyoffice.tar
ctr -n k8s.io images import onlyoffice.tar
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @onlyoffice.json

```


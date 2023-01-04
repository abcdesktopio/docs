# writer
![circle_libreoffice_writer.svg](icons/circle_libreoffice_writer.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.alpine.libreoffice](../abcdesktopio/oc.template.alpine.libreoffice)
## Distribution
alpine ![alpine](icons/alpine.svg){: style="height:32px;"}

``` 
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.17.0
PRETTY_NAME="Alpine Linux v3.17"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"

```


## Alpine packages

``` 
libreoffice-gnome
```

## Arguments
`"--writer"`
## Displayname


``` 
Writer alpine
```

## Path


``` 
/usr/lib/libreoffice/program/soffice
```

## uniquerunkey
"libreoffice"
## Showinview
"dock"
## Mimetype

``` 
application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-template;application/vnd.oasis.opendocument.text-web;application/vnd.oasis.opendocument.text-master;application/vnd.oasis.opendocument.text-master-template;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.template;application/vnd.sun.xml.writer.global;application/msword;application/vnd.ms-word;application/x-doc;application/x-hwp;application/rtf;text/rtf;application/vnd.wordperfect;application/wordperfect;application/vnd.lotus-wordpro;application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.ms-word.document.macroenabled.12;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/vnd.ms-word.template.macroenabled.12;application/vnd.stardivision.writer-global;application/x-extension-txt;application/x-t602;application/vnd.oasis.opendocument.text-flat-xml;application/x-fictionbook+xml;application/macwriteii;application/x-aportisdoc;application/prs.plucker;application/vnd.palm;application/clarisworks;application/x-sony-bbeb;application/x-abiword;application/x-iwork-pages-sffpages;application/x-mswrite;
```

## File extensions
`"sxw;stw;doc;dot;wps;rtf;602;wpd;docx;docm;dotx;dotm;abw;zabw;pages;dummy;lrf;cwk;hqx;fb2;mw;mcw;mwd;pdb;wn"`
## Legacy file extensions
`"odf;ott;fodt;uot"`
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
libreoffice.libreoffice-writer
```

> The WM_CLASS property (of type STRING without control characters) contains two consecutive null-terminated strings. These specify the Instance and Class names to be used by both the client and the window manager for looking up resources for the application or as identifying information.
> to get the WM_CLASS property of an application, use the command line `wmctrl -lx`

## Desktopfile

``` 
/usr/share/applications/libreoffice-writer.desktop
```

> A .desktop file is a simple text file that holds information about a program. It is usually placed in “/usr/share/applications/”.



## JSON dump
json source file

``` json
{
    "acl": {
        "permit": [
            "all"
        ]
    },
    "cat": "office",
    "apkpackage": "libreoffice-gnome",
    "icon": "circle_libreoffice_writer.svg",
    "keyword": "libreoffice,office",
    "launch": "libreoffice.libreoffice-writer",
    "name": "writer",
    "rules": {
        "homedir": {
            "default": true
        }
    },
    "displayname": "Writer alpine",
    "showinview": "dock",
    "path": "/usr/lib/libreoffice/program/soffice",
    "args": "--writer",
    "uniquerunkey": "libreoffice",
    "template": "abcdesktopio/oc.template.alpine.libreoffice",
    "mimetype": "application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-template;application/vnd.oasis.opendocument.text-web;application/vnd.oasis.opendocument.text-master;application/vnd.oasis.opendocument.text-master-template;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.template;application/vnd.sun.xml.writer.global;application/msword;application/vnd.ms-word;application/x-doc;application/x-hwp;application/rtf;text/rtf;application/vnd.wordperfect;application/wordperfect;application/vnd.lotus-wordpro;application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.ms-word.document.macroenabled.12;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/vnd.ms-word.template.macroenabled.12;application/vnd.stardivision.writer-global;application/x-extension-txt;application/x-t602;application/vnd.oasis.opendocument.text-flat-xml;application/x-fictionbook+xml;application/macwriteii;application/x-aportisdoc;application/prs.plucker;application/vnd.palm;application/clarisworks;application/x-sony-bbeb;application/x-abiword;application/x-iwork-pages-sffpages;application/x-mswrite;",
    "legacyfileextensions": "odf;ott;fodt;uot",
    "fileextensions": "sxw;stw;doc;dot;wps;rtf;602;wpd;docx;docm;dotx;dotm;abw;zabw;pages;dummy;lrf;cwk;hqx;fb2;mw;mcw;mwd;pdb;wn",
    "desktopfile": "/usr/share/applications/libreoffice-writer.desktop",
    "usedefaultapplication": true,
    "abcdesktop_release": 3
}
```

## Install the builded image
>Replace the **ABCHOST** var set to localhost by default to your own server ip address

``` sh
ABCHOST=localhost
curl --output writer.json https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/writer.d.3.0.json
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @writer.json

```

## Generated `DockerFile` source code

``` 
# Dynamic DockerFile application file for abcdesktopio generated by abcdesktopio/oc.apps/make.js
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
ARG TAG=dev
FROM abcdesktopio/oc.template.alpine.libreoffice:$TAG
USER root
RUN apk add --no-cache --update libreoffice-gnome
LABEL oc.icon="circle_libreoffice_writer.svg"
LABEL oc.icondata="PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiA8ZGVmcz4KICA8bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgxPSIzOTkuNTciIHgyPSIzOTkuNTciIHkxPSI1NDUuOCIgeTI9IjUxNy44IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDIuMTQyOSwwLDAsMi4xNDI5LC04MjYuMzYsLTExMDcuNSkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KICAgPHN0b3Agc3RvcC1jb2xvcj0iIzM4ODllOSIgb2Zmc2V0PSIwIi8+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiM1ZWE1ZmIiIG9mZnNldD0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiAgPGZpbHRlciBpZD0iYyIgeD0iLS4wMzYiIHk9Ii0uMDM2IiB3aWR0aD0iMS4wNzIiIGhlaWdodD0iMS4wNzIiIGNvbG9yLWludGVycG9sYXRpb24tZmlsdGVycz0ic1JHQiI+CiAgIDxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjAuNDE5OTk4NzQiLz4KICA8L2ZpbHRlcj4KICA8bGluZWFyR3JhZGllbnQgaWQ9ImgiIHgxPSIzNDUiIHgyPSIzNDUiIHkxPSIxMTczIiB5Mj0iMTE3OCIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgyLjEyNSAwIDAgMi4xMzc0IC03MDIuMTIgLTI0ODcuOSkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KICAgPHN0b3Agc3RvcC1jb2xvcj0iIzY2NiIgb2Zmc2V0PSIwIi8+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiMzMzMiIG9mZnNldD0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJpIiB4MT0iMjI5LjUzIiB4Mj0iMjI5LjUzIiB5MT0iLTU4MS42NCIgeTI9Ii01NzguNjQiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMi4xMjUgMCAwIDIgLTQ0MC43NSAxMTgxLjMpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiM2M2JiZWUiIG9mZnNldD0iMCIvPgogICA8c3RvcCBzdG9wLWNvbG9yPSIjYWFkY2Y3IiBvZmZzZXQ9IjEiLz4KICA8L2xpbmVhckdyYWRpZW50PgogIDxsaW5lYXJHcmFkaWVudCBpZD0iaiIgeDE9IjIxNy4yOSIgeDI9IjIxNy4yOSIgeTE9Ii03ODcuODQiIHkyPSItNzYzLjg0IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDIuMTY4MyAwIDAgMi4zMjMzIC00MzguODcgMTgzMC42KSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiIHhsaW5rOmhyZWY9IiNhIi8+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJhIj4KICAgPHN0b3Agc3RvcC1jb2xvcj0iIzAzNjlhMyIgb2Zmc2V0PSIwIi8+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiMwNDdmYzYiIG9mZnNldD0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJnIiB4MT0iMzIuMDIiIHgyPSIzMi4wMiIgeTE9IjIuMDQzIiB5Mj0iNjIuMDQ1IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeGxpbms6aHJlZj0iI2EiLz4KICA8bGluZWFyR3JhZGllbnQgaWQ9ImYiIHgxPSIzMiIgeDI9IjMyIiB5MT0iNyIgeTI9IjU3IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiNkMmYzZmMiIG9mZnNldD0iMCIvPgogICA8c3RvcCBzdG9wLWNvbG9yPSIjZmZmIiBvZmZzZXQ9IjEiLz4KICA8L2xpbmVhckdyYWRpZW50PgogIDxsaW5lYXJHcmFkaWVudCBpZD0iZSIgeDE9IjQ1LjUwMSIgeDI9IjQ1LjUwMSIgeTE9IjcuMTA1NSIgeTI9IjI5Ljg5NiIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgogICA8c3RvcCBzdG9wLWNvbG9yPSIjZWJmYWZlIiBvZmZzZXQ9IjAiLz4KICAgPHN0b3Agc3RvcC1jb2xvcj0iI2U3ZjhmYyIgb2Zmc2V0PSIxIi8+CiAgPC9saW5lYXJHcmFkaWVudD4KICA8ZmlsdGVyIGlkPSJrIiB4PSItLjAzNiIgeT0iLS4wMzYiIHdpZHRoPSIxLjA3MiIgaGVpZ2h0PSIxLjA3MiIgY29sb3ItaW50ZXJwb2xhdGlvbi1maWx0ZXJzPSJzUkdCIj4KICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMC43NSIvPgogIDwvZmlsdGVyPgogIDxyYWRpYWxHcmFkaWVudCBpZD0iZCIgY3g9IjM4LjA2NiIgY3k9IjI2LjE5MiIgcj0iMjUiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoLS44IDIuOTg4NmUtOCAtMS45MjY1ZS04IC0xIDgwLjQ1MyA0MC4xOTIpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiMxZTM1M2MiIHN0b3Atb3BhY2l0eT0iLjQ4NTM4IiBvZmZzZXQ9IjAiLz4KICAgPHN0b3Agc3RvcC1jb2xvcj0iIzE5MTkxOSIgc3RvcC1vcGFjaXR5PSIwIiBvZmZzZXQ9IjEiLz4KICA8L3JhZGlhbEdyYWRpZW50PgogIDxmaWx0ZXIgaWQ9ImwiIHg9Ii0uMDU2MzY0IiB5PSItLjA2NDEzOCIgd2lkdGg9IjEuMTEyNyIgaGVpZ2h0PSIxLjEyODMiIGNvbG9yLWludGVycG9sYXRpb24tZmlsdGVycz0ic1JHQiI+CiAgIDxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjAuNzc1Ii8+CiAgPC9maWx0ZXI+CiA8L2RlZnM+CiA8Y2lyY2xlIHRyYW5zZm9ybT0ibWF0cml4KDIuMTQyOSAwIDAgMi4xNDI5IC04MjYuMzYgLTExMDcuNSkiIGN4PSI0MDAuNTciIGN5PSI1MzEuOCIgcj0iMTQiIGZpbHRlcj0idXJsKCNjKSIgb3BhY2l0eT0iLjI1IiBzdHJva2Utd2lkdGg9Ii43MzMzMyIvPgogPGcgc3Ryb2tlLXdpZHRoPSIxLjU3MTUiPgogIDxjaXJjbGUgY3g9IjMyLjAyIiBjeT0iMzIuMDQ0IiByPSIzMC4wMDEiIGZpbGw9InVybCgjZykiLz4KICA8cGF0aCBkPSJtMzIgN2EyNSAyNSAwIDAgMC0yNSAyNSAyNSAyNSAwIDAgMCAyNSAyNSAyNSAyNSAwIDAgMCAyNS0yNSAyNSAyNSAwIDAgMC0wLjEwMzUyLTIuMTAzNWwtMjIuNzkxLTIyLjc5MWEyNSAyNSAwIDAgMC0yLjEwNTUtMC4xMDU0N3oiIGZpbHRlcj0idXJsKCNrKSIgb3BhY2l0eT0iLjI1Ii8+CiAgPGNpcmNsZSBjeD0iMzIuMDIiIGN5PSIzMi4wNDQiIHI9IjMwLjAwMSIgZmlsbC1vcGFjaXR5PSIwIi8+CiAgPGNpcmNsZSBjeD0iMzIuMDIiIGN5PSIzMi4wNDQiIHI9IjAiIGZpbGw9InVybCgjYikiLz4KICA8cGF0aCBkPSJtMzIgN2EyNSAyNSAwIDAgMC0yNSAyNSAyNSAyNSAwIDAgMCAyNSAyNSAyNSAyNSAwIDAgMCAyNS0yNSAyNSAyNSAwIDAgMC0wLjEwMzUyLTIuMTAzNWwtMjIuNzkxLTIyLjc5MWEyNSAyNSAwIDAgMC0yLjEwNTUtMC4xMDU0N3oiIGZpbGw9InVybCgjZikiLz4KIDwvZz4KIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAsMSkiIGZpbHRlcj0idXJsKCNsKSIgb3BhY2l0eT0iLjI1Ij4KICA8cGF0aCBkPSJtMTYgMTd2M2gxMXYtM3ptMTQgMHYxNGgxOXYtN2MtMy0zLTUtNC05LjUtN3ptLTE0IDV2My4wNDc5bDExLTAuMDQ3OTR2LTMuMDQ3OXptMCA1djMuMDQ3OWwxMS0wLjA0Nzk0di0zLjA0Nzl6bTAgNnYzbDMzLTAuMDQ3OTR2LTN6bTAgNXYzbDMzLTAuMDQ3OTR2LTN6bTAgNXYzaDI0di0zeiIgY29sb3I9IiMwMDAwMDAiIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXciLz4KICA8cGF0aCBkPSJtMzEgMThoOC41YzMuNSAwIDguNSA0IDguNSA2djZoLTE3eiIgY29sb3I9IiMwMDAwMDAiIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXciLz4KICA8cGF0aCBkPSJtNDAuOTE3IDI3LjIxMi00LjkxNy02LjIxMjEtNSA3LjYwNjF2MS4zOTM5aDE3di0xLjM5MzlsLTMuNTQxMy00LjE4MTh6IiBjb2xvcj0iIzAwMDAwMCIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyIvPgogPC9nPgogPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwxKSI+CiAgPHBhdGggZD0ibTE2IDE3djNoMTF2LTN6bTE0IDB2MTRoMTl2LTdjLTMtMy01LTQtOS41LTd6bS0xNCA1djMuMDQ3OWwxMS0wLjA0Nzk0di0zLjA0Nzl6bTAgNXYzLjA0NzlsMTEtMC4wNDc5NHYtMy4wNDc5em0wIDZ2M2wzMy0wLjA0Nzk0di0zem0wIDV2M2wzMy0wLjA0Nzk0di0zem0wIDV2M2gyNHYtM3oiIGNvbG9yPSIjMDAwMDAwIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IiBmaWxsPSJ1cmwoI2opIi8+CiAgPHBhdGggZD0ibTMxIDE4aDguNWMzLjUgMCA4LjUgNCA4LjUgNnY2aC0xN3oiIGNvbG9yPSIjMDAwMDAwIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IiBmaWxsPSJ1cmwoI2kpIi8+CiAgPHBhdGggZD0ibTQwLjkxNyAyNy4yMTItNC45MTctNi4yMTIxLTUgNy42MDYxdjEuMzkzOWgxN3YtMS4zOTM5bC0zLjU0MTMtNC4xODE4eiIgY29sb3I9IiMwMDAwMDAiIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXciIGZpbGw9InVybCgjaCkiLz4KIDwvZz4KIDxwYXRoIGQ9Im0zMiA3YTI1IDI1IDAgMCAwLTI1IDI1IDI1IDI1IDAgMCAwIDI1IDI1IDI1IDI1IDAgMCAwIDI1LTI1IDI1IDI1IDAgMCAwLTAuMTAzNTItMi4xMDM1bC0yMi43OTEtMjIuNzkxYTI1IDI1IDAgMCAwLTIuMTA1NS0wLjEwNTQ3eiIgZmlsbD0idXJsKCNkKSIgc3Ryb2tlLXdpZHRoPSIxLjU3MTUiLz4KIDxwYXRoIGQ9Im01Ni44OTYgMjkuODk2LTIyLjc5MS0yMi43OTFhMjUgMjUgMCAwIDAgMjIuNzkxIDIyLjc5MXoiIGZpbGw9InVybCgjZSkiIHN0cm9rZS13aWR0aD0iMS41NzE1Ii8+Cjwvc3ZnPgo="
LABEL oc.keyword="writer,libreoffice,office"
LABEL oc.cat="office"
LABEL oc.desktopfile="libreoffice-writer.desktop"
LABEL oc.launch="libreoffice.libreoffice-writer"
LABEL oc.template="abcdesktopio/oc.template.alpine.libreoffice"
ENV ARGS="--writer"
LABEL oc.name="writer"
LABEL oc.displayname="Writer alpine"
LABEL oc.path="/usr/lib/libreoffice/program/soffice"
LABEL oc.type=app
LABEL oc.uniquerunkey="libreoffice"
LABEL oc.showinview="dock"
LABEL oc.mimetype="application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-template;application/vnd.oasis.opendocument.text-web;application/vnd.oasis.opendocument.text-master;application/vnd.oasis.opendocument.text-master-template;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.template;application/vnd.sun.xml.writer.global;application/msword;application/vnd.ms-word;application/x-doc;application/x-hwp;application/rtf;text/rtf;application/vnd.wordperfect;application/wordperfect;application/vnd.lotus-wordpro;application/vnd.openxmlformats-officedocument.wordprocessingml.document;application/vnd.ms-word.document.macroenabled.12;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/vnd.ms-word.template.macroenabled.12;application/vnd.stardivision.writer-global;application/x-extension-txt;application/x-t602;application/vnd.oasis.opendocument.text-flat-xml;application/x-fictionbook+xml;application/macwriteii;application/x-aportisdoc;application/prs.plucker;application/vnd.palm;application/clarisworks;application/x-sony-bbeb;application/x-abiword;application/x-iwork-pages-sffpages;application/x-mswrite;"
LABEL oc.fileextensions="sxw;stw;doc;dot;wps;rtf;602;wpd;docx;docm;dotx;dotm;abw;zabw;pages;dummy;lrf;cwk;hqx;fb2;mw;mcw;mwd;pdb;wn"
LABEL oc.legacyfileextensions="odf;ott;fodt;uot"
LABEL oc.rules="{\"homedir\":{\"default\":true}}"
LABEL oc.acl="{\"permit\":[\"all\"]}"
RUN  if [ -d /usr/share/icons ]   && [ -x /composer/safelinks.sh ] && [ -d /usr/share/icons   ];  then cd /usr/share/icons;    /composer/safelinks.sh; fi 
RUN  if [ -d /usr/share/pixmaps ] && [ -x /composer/safelinks.sh ] && [ -d /usr/share/pixmaps ];  then cd /usr/share/pixmaps;  /composer/safelinks.sh; fi 
ENV APPNAME "writer"
ENV APPBIN "/usr/lib/libreoffice/program/soffice"
LABEL oc.args="--writer"
ENV APP "/usr/lib/libreoffice/program/soffice"
LABEL oc.usedefaultapplication=true
USER root
RUN mkdir -p /var/secrets/abcdesktop/localaccount && cp /etc/passwd /etc/group /etc/shadow /var/secrets/abcdesktop/localaccount
RUN rm -f /etc/passwd && ln -s /var/secrets/abcdesktop/localaccount/passwd /etc/passwd
RUN rm -f /etc/group && ln -s /var/secrets/abcdesktop/localaccount/group  /etc/group
RUN rm -f /etc/shadow && ln -s /var/secrets/abcdesktop/localaccount/shadow /etc/shadow
RUN rm -f /etc/gshadow && ln -s /var/secrets/abcdesktop/localaccount/gshadow /etc/gshadow
USER balloon
CMD [ "/composer/appli-docker-entrypoint.sh" ]

```

## Rebuild the image manually

### Download the Dockerfile manually
[Dockerfile for application writer](https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/writer.d)
``` sh
wget https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/writer.d
```

### build the `Dockerfile` to create a container image

``` sh
docker build --build-arg TAG=3.0 -f writer.d -t writer .
```

### Install the new image
>If you are using `containerd` as container runtime, use the ctr command line

 
>If you are not running this bash command on your abcdesktop node
>Replace the **ABCHOST** variable set to localhost by default to your own server ip address


``` sh
ABCHOST=localhost
docker inspect writer > writer.json
docker image save writer -o writer.tar
ctr -n k8s.io images import writer.tar
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @writer.json

```


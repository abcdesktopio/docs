# hyper
![hyper.svg](icons/hyper.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](../abcdesktopio/oc.template.ubuntu.minimal.22.04)
## Path


``` 
/opt/Hyper/hyper
```

## Mimetype

``` 
x-scheme-handler/ssh
```

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
hyper.Hyper
```

> The WM_CLASS property (of type STRING without control characters) contains two consecutive null-terminated strings. These specify the Instance and Class names to be used by both the client and the window manager for looking up resources for the application or as identifying information.
> to get the WM_CLASS property of an application, use the command line `wmctrl -lx`

## Desktopfile

``` 
/usr/share/applications/hyper.desktop
```

> A .desktop file is a simple text file that holds information about a program. It is usually placed in “/usr/share/applications/”.

## PRE run command

> PRE run command are run **before** the package install command

```
RUN apt-get update && apt-get install  --no-install-recommends --yes libgtk-3-0 libx11-xcb1 libasound2 && apt-get clean
RUN curl -Ls -o /tmp/hyper.deb  https://releases.hyper.is/download/deb && apt-get install  --no-install-recommends --yes /tmp/hyper.deb && apt-get clean && rm -rf /tmp/hyper.deb
```



## JSON dump
json source file hyper.d.3.0.json 

``` json
{
    "acl": {
        "permit": [
            "all"
        ]
    },
    "cat": "utilities",
    "debpackage": "",
    "preruncommands": [
        "RUN apt-get update && apt-get install  --no-install-recommends --yes libgtk-3-0 libx11-xcb1 libasound2 && apt-get clean",
        "RUN curl -Ls -o /tmp/hyper.deb  https://releases.hyper.is/download/deb && apt-get install  --no-install-recommends --yes /tmp/hyper.deb && apt-get clean && rm -rf /tmp/hyper.deb"
    ],
    "icon": "hyper.svg",
    "keyword": "terminal,remote",
    "launch": "hyper.Hyper",
    "name": "hyper",
    "path": "/opt/Hyper/hyper",
    "mimetype": "x-scheme-handler/ssh",
    "fileextensions": "",
    "template": "abcdesktopio/oc.template.ubuntu.minimal.22.04",
    "rules": {
        "homedir": {
            "default": true
        }
    },
    "desktopfile": "/usr/share/applications/hyper.desktop"
}
```

## Install the builded image
>Replace the **ABCHOST** var set to localhost by default to your own server ip address

``` sh
ABCHOST=localhost
curl --output hyper.d.3.0.json https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/hyper.d.3.0.json
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @hyper.d.3.0.json

```

## Generated `DockerFile` source code

``` 
# Dynamic DockerFile application file for abcdesktopio generated by abcdesktopio/oc.apps/make.js
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
ARG TAG=dev
FROM abcdesktopio/oc.template.ubuntu.minimal.22.04:$TAG
USER root
RUN apt-get update && apt-get install  --no-install-recommends --yes libgtk-3-0 libx11-xcb1 libasound2 && apt-get clean
RUN curl -Ls -o /tmp/hyper.deb  https://releases.hyper.is/download/deb && apt-get install  --no-install-recommends --yes /tmp/hyper.deb && apt-get clean && rm -rf /tmp/hyper.deb
LABEL oc.icon="hyper.svg"
LABEL oc.icondata="PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZlcnNpb249IjEuMSIgdmlld0JveD0iMCAwIDQ4IDQ4LjAwMDAwMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KIDxkZWZzPgogIDxsaW5lYXJHcmFkaWVudCBpZD0ibGluZWFyR3JhZGllbnQ0NTAxIiB4MT0iLTQ3IiB4Mj0iLTEiIHkxPSIyLjg3NzllLTE1IiB5Mj0iNi4xMjMyZS0xNyIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgogICA8c3RvcCBzdHlsZT0ic3RvcC1jb2xvcjojM2QzZDNkIiBvZmZzZXQ9IjAiLz4KICAgPHN0b3Agc3R5bGU9InN0b3AtY29sb3I6IzQ3NDc0NyIgb2Zmc2V0PSIxIi8+CiAgPC9saW5lYXJHcmFkaWVudD4KIDwvZGVmcz4KIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMy45NDllLTUpIj4KICA8cGF0aCBkPSJtMSA0M3YwLjI1YzAgMi4yMTYgMS43ODQgNCA0IDRoMzhjMi4yMTYgMCA0LTEuNzg0IDQtNHYtMC4yNWMwIDIuMjE2LTEuNzg0IDQtNCA0aC0zOGMtMi4yMTYgMC00LTEuNzg0LTQtNHptMCAwLjV2MC41YzAgMi4yMTYgMS43ODQgNCA0IDRoMzhjMi4yMTYgMCA0LTEuNzg0IDQtNHYtMC41YzAgMi4yMTYtMS43ODQgNC00IDRoLTM4Yy0yLjIxNiAwLTQtMS43ODQtNC00eiIgc3R5bGU9Im9wYWNpdHk6LjAyIi8+CiAgPHBhdGggZD0ibTEgNDMuMjV2MC4yNWMwIDIuMjE2IDEuNzg0IDQgNCA0aDM4YzIuMjE2IDAgNC0xLjc4NCA0LTR2LTAuMjVjMCAyLjIxNi0xLjc4NCA0LTQgNGgtMzhjLTIuMjE2IDAtNC0xLjc4NC00LTR6IiBzdHlsZT0ib3BhY2l0eTouMDUiLz4KICA8cGF0aCBkPSJtMSA0M3YwLjI1YzAgMi4yMTYgMS43ODQgNCA0IDRoMzhjMi4yMTYgMCA0LTEuNzg0IDQtNHYtMC4yNWMwIDIuMjE2LTEuNzg0IDQtNCA0aC0zOGMtMi4yMTYgMC00LTEuNzg0LTQtNHoiIHN0eWxlPSJvcGFjaXR5Oi4xIi8+CiA8L2c+CiA8cmVjdCB0cmFuc2Zvcm09InJvdGF0ZSgtOTApIiB4PSItNDciIHk9IjEiIHdpZHRoPSI0NiIgaGVpZ2h0PSI0NiIgcng9IjQiIHN0eWxlPSJmaWxsOnVybCgjbGluZWFyR3JhZGllbnQ0NTAxKSIvPgogPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCAzLjk0OWUtNSkiPgogIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgLTEwMDQuNCkiPgogICA8cGF0aCBkPSJtMSAxMDQzLjR2NGMwIDIuMjE2IDEuNzg0IDQgNCA0aDM4YzIuMjE2IDAgNC0xLjc4NCA0LTR2LTRjMCAyLjIxNi0xLjc4NCA0LTQgNGgtMzhjLTIuMjE2IDAtNC0xLjc4NC00LTR6IiBzdHlsZT0ib3BhY2l0eTouMSIvPgogIDwvZz4KIDwvZz4KIDxwYXRoIGQ9Im0yMyAxMi0xMSA5IDUgMy0zIDggMTAtOS01LTN6bTIgMTh2MmgxMHYtMnoiIHN0eWxlPSJvcGFjaXR5Oi4xIi8+CiA8cGF0aCBkPSJtMzUgMzF2LTJoLTEwdjJtMTAgMCIgc3R5bGU9ImZpbGw6I2Y0NjA5ZCIvPgogPHBhdGggZD0ibTEyIDIwIDExLTktNCA4IDUgMy0xMCA5IDMtOHoiIHN0eWxlPSJmaWxsOiNmMWFiNDUiLz4KIDxwYXRoIGQ9Im0xMiAyMCAxMS05LTQgOCA1IDMtMTAgOSAzLTh6IiBzdHlsZT0iZmlsbDojZjNiNjRkIi8+Cjwvc3ZnPgo="
LABEL oc.keyword="hyper,terminal,remote"
LABEL oc.cat="utilities"
LABEL oc.desktopfile="hyper.desktop"
LABEL oc.launch="hyper.Hyper"
LABEL oc.template="abcdesktopio/oc.template.ubuntu.minimal.22.04"
LABEL oc.name="hyper"
LABEL oc.displayname="hyper"
LABEL oc.path="/opt/Hyper/hyper"
LABEL oc.type=app
LABEL oc.mimetype="x-scheme-handler/ssh"
LABEL oc.rules="{\"homedir\":{\"default\":true}}"
LABEL oc.acl="{\"permit\":[\"all\"]}"
RUN for d in /usr/share/icons /usr/share/pixmaps ; do echo "testing link in $d"; if [ -d $d ] && [ -x /composer/safelinks.sh ] ; then echo "fixing link in $d"; cd $d ; /composer/safelinks.sh ; fi; done
ENV APPNAME "hyper"
ENV APPBIN "/opt/Hyper/hyper"
ENV APP "/opt/Hyper/hyper"
USER root
RUN mkdir -p /var/secrets/abcdesktop/localaccount
RUN for f in passwd shadow group gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /var/secrets/abcdesktop/localaccount; rm -f /etc/$f; ln -s /var/secrets/abcdesktop/localaccount/$f /etc/$f; fi; done
USER balloon
CMD [ "/composer/appli-docker-entrypoint.sh" ]

```

## Rebuild the image manually

### Download the Dockerfile manually
[Dockerfile for application hyper](https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/hyper.d)
``` sh
wget https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/hyper.d
```

### build the `Dockerfile` to create a container image

``` sh
docker build --build-arg TAG=3.0 -f hyper.d -t hyper .
```

### Install the new image
>If you are using `containerd` as container runtime, use the ctr command line

 
>If you are not running this bash command on your abcdesktop node
>Replace the **ABCHOST** variable set to localhost by default to your own server ip address


``` sh
ABCHOST=localhost
docker inspect hyper > hyper.json
docker image save hyper -o hyper.tar
ctr -n k8s.io images import hyper.tar
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @hyper.json

```


# evolution
![evolution.svg](icons/evolution.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](../abcdesktopio/oc.template.ubuntu.minimal.22.04)
## Distribution
ubuntu ![ubuntu](icons/ubuntu.svg){: style="height:32px;"}

``` 
PRETTY_NAME="Ubuntu 22.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.1 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy

```


## Ubuntu packages

``` 
evolution dbus-x11
```

## Displayname


``` 
Evolution
```

## Path


``` 
/usr/bin/evolution
```

## Mimetype

``` 
text/calendar;text/x-vcard;text/directory;application/mbox;message/rfc822;x-scheme-handler/mailto;
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
evolution.Evolution
```

> The WM_CLASS property (of type STRING without control characters) contains two consecutive null-terminated strings. These specify the Instance and Class names to be used by both the client and the window manager for looking up resources for the application or as identifying information.
> to get the WM_CLASS property of an application, use the command line `wmctrl -lx`

## Desktopfile

``` 
/usr/share/applications/org.gnome.Evolution.desktop
```

> A .desktop file is a simple text file that holds information about a program. It is usually placed in “/usr/share/applications/”.



## JSON dump
json source file evolution.d.3.0.json 

``` json
{
    "acl": {
        "permit": [
            "all"
        ]
    },
    "cat": "office",
    "debpackage": "evolution dbus-x11",
    "icon": "evolution.svg",
    "keyword": "evolution,mail",
    "launch": "evolution.Evolution",
    "name": "evolution",
    "displayname": "Evolution",
    "path": "/usr/bin/evolution",
    "rules": {
        "homedir": {
            "default": true
        }
    },
    "template": "abcdesktopio/oc.template.ubuntu.minimal.22.04",
    "mimetype": "text/calendar;text/x-vcard;text/directory;application/mbox;message/rfc822;x-scheme-handler/mailto;",
    "desktopfile": "/usr/share/applications/org.gnome.Evolution.desktop"
}
```

## Install the builded image
>Replace the **ABCHOST** var set to localhost by default to your own server ip address

``` sh
ABCHOST=localhost
curl --output evolution.d.3.0.json https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/evolution.d.3.0.json
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @evolution.d.3.0.json

```

## Generated `DockerFile` source code

``` 
# Dynamic DockerFile application file for abcdesktopio generated by abcdesktopio/oc.apps/make.js
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
ARG TAG=dev
FROM abcdesktopio/oc.template.ubuntu.minimal.22.04:$TAG
USER root
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y  --no-install-recommends evolution dbus-x11 && apt-get clean
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
LABEL oc.icon="evolution.svg"
LABEL oc.icondata="PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgd2lkdGg9IjQ4IiBoZWlnaHQ9IjQ4Ij4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzlhYTI5YSIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNiNWJlYjUiLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgICA8cmFkaWFsR3JhZGllbnQgaWQ9ImIiIGN4PSI2LjcwMyIgY3k9IjczLjYxNiIgcj0iNy4yMjgiIGdyYWRpZW50VHJhbnNmb3JtPSJzY2FsZSgxLjkwMjIgLjUyNTcpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEiIHN0b3Atb3BhY2l0eT0iMCIvPgogICAgPC9yYWRpYWxHcmFkaWVudD4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iaSIgeDE9IjguNzgiIHgyPSI5Ljc2MiIgeTE9IjM3Ljc4NSIgeTI9IjMyLjIwMyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgyLjM5NDkgMCAwIC43ODEwNiAyLjg4IC4zNDMpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1vcGFjaXR5PSIuMTI5Ii8+CiAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1vcGFjaXR5PSIwIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJoIiB4MT0iMTEuMjMzIiB4Mj0iMjEuMTEyIiB5MT0iMTMuNjg2IiB5Mj0iMjQuMTMzIiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDEuMzcwOSAwIDAgMS40NDM4IDIuNDMxIC0uMTQpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iI2ZmZiIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNlZGVkZWQiLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImciIHgxPSI4LjkxNiIgeDI9IjkuODg2IiB5MT0iMzcuMTk3IiB5Mj0iNTIuMDkxIiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDIuNDU0OCAwIDAgLjc2MiAyLjg4IC4zNDMpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeGxpbms6aHJlZj0iI2EiLz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZiIgeDE9IjEwLjE4NCIgeDI9IjE1LjMxMSIgeTE9IjE1LjE0OCIgeTI9IjI5LjU2OSIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxLjgxOTMgMCAwIDEuMDI4MiAyLjg4IC4zNDMpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iI2ZmZiIvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNkY2RjZGMiLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImUiIHgxPSI1LjgyNyIgeDI9IjEzLjQ2NyIgeTE9IjcuMjMxIiB5Mj0iMTcuODc3IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDEuNTcwNiAwIDAgMS4xOTEgMi44OCAuMzQzKSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNlZGVkZWQiLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjYzhjOGM4Ii8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJjIiB4MT0iMTEuNTczIiB4Mj0iMTguNDc1IiB5MT0iNC43NDYiIHkyPSIyNi4wMjMiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMS4zNDM1IDAgMCAxLjQxNzkgMi44OCAuMzE1KSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNmZmYiLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjZTJlMmUyIi8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJkIiB4MT0iMi4wNjIiIHgyPSIzMC42IiB5MT0iMTUuMjU3IiB5Mj0iMTUuMjU3IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KDEuMzQzNSAwIDAgMS40MTc5IDIuODggLjMxNSkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KICAgICAgPHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjOTg5NjkwIi8+CiAgICAgIDxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzY1NjQ2MCIvPgogICAgPC9saW5lYXJHcmFkaWVudD4KICA8L2RlZnM+CiAgPHBhdGggZmlsbD0idXJsKCNiKSIgZD0iTTI2LjUgMzguN2ExMy43NSAzLjggMCAxIDEtMjcuNSAwIDEzLjc1IDMuOCAwIDEgMSAyNy41IDB6IiBjb2xvcj0iIzAwMCIgb3BhY2l0eT0iLjQ1NiIgdHJhbnNmb3JtPSJtYXRyaXgoMS44MDA2IDAgMCAxLjk3NDggMS4wODQgLTM4LjAxMykiLz4KICA8cGF0aCBmaWxsPSJ1cmwoI2MpIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZT0idXJsKCNkKSIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSIuODU3IiBkPSJNNi4zMzMgMTYuOTcydjI0LjUxaDM2Ljk3M2wtLjA2Mi0yNC4zOTJjLS4wMDMtMS4zNzgtMTEuODQ4LTE0LjY3OC0xNC4wMzMtMTQuNjc4SDIwLjY2Yy0yLjI5NyAwLTE0LjMyNiAxMy4yNjItMTQuMzI2IDE0LjU2eiIvPgogIDxwYXRoIGZpbGw9InVybCgjZSkiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTYuOTIzIDE2Ljc4N2MtLjM5OC0uNDMgMTEuODg3LTEzLjY5NCAxMy43NDQtMTMuNjk0aDguMzc2YzEuNzQ3IDAgMTQuMDM3IDEzLjEyOCAxMy40MjcgMTMuODg2TDMxLjYxIDMwLjQ3NGwtMTIuMzE1LS4zMTgtMTIuMzcyLTEzLjM3eiIvPgogIDxwYXRoIGZpbGwtb3BhY2l0eT0iLjE0NiIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTkuMDc4IDMwLjAxOGwtNy4zMzMtOC43NDYgMjQuODE4LTYuOTM2IDMuMDI5IDYuMjE2LTcuNDE2IDkuNDQiLz4KICA8cGF0aCBmaWxsLW9wYWNpdHk9Ii4xNDYiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTE4LjI5MiAyOS44MzZsLTcuNDgzLTguODEgMjQuNjQ4LTYuODkzIDMuMTc0IDYuMjcxLTcuMjQxIDkuNDA3Ii8+CiAgPHBhdGggZmlsbC1vcGFjaXR5PSIuMTQ2IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xOC43NzUgMjkuOTU3bC03LjY3NS04LjY2IDI0Ljk2OC03LjA2NSAzLjI4NiA2LjU5My03LjQ4IDkuMTA3Ii8+CiAgPHBhdGggZmlsbD0idXJsKCNmKSIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTguNTk0IDMwLjQ0MWwtNy4zMzMtOC43NDYgMjQuNzEyLTYuODk0IDMuMTEgNi4zODgtNy4xMiA4Ljk4NiIvPgogIDxwYXRoIGZpbGw9InVybCgjZykiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTIwLjQ4OCAyOS4wNjRMNy4wOTIgNDAuMDM2bDEzLjkwOS05LjYwNGg5LjAxOGwxMi40MiA5LjQ4Mi0xMS44NjQtMTAuODVIMjAuNDg4eiIvPgogIDxwYXRoIGZpbGw9InVybCgjZykiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTYuOTYzIDE2Ljg4NUwxOC40OCAzMS4yMDFsMS4wNjgtLjg1NEw2Ljk2NCAxNi44ODV6IiBjb2xvcj0iIzAwMCIvPgogIDxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0idXJsKCNoKSIgc3Ryb2tlLXdpZHRoPSIuODU3IiBkPSJNNy4zMDggMTcuMTMxbC4wMyAyMy4yMTFoMzQuOTQ2bC0uMDYzLTIzLjA4NGMtLjAwMi0uNzUtMTEuMjE2LTEzLjc5OS0xMy4zODQtMTMuNzk5aC03Ljg5NWMtMi4yNTMgMC0xMy42MzUgMTIuODkyLTEzLjYzNCAxMy42NzJ6Ii8+CiAgPHBhdGggZmlsbD0iI2ZmZiIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMjAuOTU3IDMwLjQ1M0w5LjAxNiAzOC43MjRsMi4yMTkuMDA2IDkuOTk4LTYuODY5IDguODIyLTEuNDIzLTkuMDk4LjAxNXptLTkuNTI5LTguNzgzbDEuMzI0IDEuNDExIDIyLjc5MS02Ljg4NCAyLjkxNSA1LjY4Mi42MTQtLjcxMi0zLjA2OS02LjM3OC0yNC41NzUgNi44ODF6Ii8+CiAgPHBhdGggZmlsbD0idXJsKCNpKSIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTMuMzA4IDIzLjYzNmw2LjAyNiA2LjQ1NCAxLjE5Ny0xLjAyNiAxMC4wODcuMDQzLjgxMi43MjcgMy45NzUtNC43NDRjLTEuMTU0LTEuNDExLTIyLjA5Ny0xLjQ1NC0yMi4wOTctMS40NTR6Ii8+CiAgPHBhdGggZmlsbD0iI2IxYjFiMSIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNNDEuODEzIDE3Ljg0OGwtOS45NTIgMTIuNjMxLTEuMDY4LS44NTUgMTEuMDItMTEuNzc2eiIgY29sb3I9IiMwMDAiLz4KPC9zdmc+Cg=="
LABEL oc.keyword="evolution,evolution,mail"
LABEL oc.cat="office"
LABEL oc.desktopfile="org.gnome.Evolution.desktop"
LABEL oc.launch="evolution.Evolution"
LABEL oc.template="abcdesktopio/oc.template.ubuntu.minimal.22.04"
LABEL oc.name="evolution"
LABEL oc.displayname="Evolution"
LABEL oc.path="/usr/bin/evolution"
LABEL oc.type=app
LABEL oc.mimetype="text/calendar;text/x-vcard;text/directory;application/mbox;message/rfc822;x-scheme-handler/mailto;"
LABEL oc.rules="{\"homedir\":{\"default\":true}}"
LABEL oc.acl="{\"permit\":[\"all\"]}"
RUN for d in /usr/share/icons /usr/share/pixmaps ; do echo "testing link in $d"; if [ -d $d ] && [ -x /composer/safelinks.sh ] ; then echo "fixing link in $d"; cd $d ; /composer/safelinks.sh ; fi; done
ENV APPNAME "evolution"
ENV APPBIN "/usr/bin/evolution"
ENV APP "/usr/bin/evolution"
USER root
RUN mkdir -p /var/secrets/abcdesktop/localaccount
RUN for f in passwd shadow group gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /var/secrets/abcdesktop/localaccount; rm -f /etc/$f; ln -s /var/secrets/abcdesktop/localaccount/$f /etc/$f; fi; done
USER balloon
CMD [ "/composer/appli-docker-entrypoint.sh" ]

```

## Rebuild the image manually

### Download the Dockerfile manually
[Dockerfile for application evolution](https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/evolution.d)
``` sh
wget https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/evolution.d
```

### build the `Dockerfile` to create a container image

``` sh
docker build --build-arg TAG=3.0 -f evolution.d -t evolution .
```

### Install the new image
>If you are using `containerd` as container runtime, use the ctr command line

 
>If you are not running this bash command on your abcdesktop node
>Replace the **ABCHOST** variable set to localhost by default to your own server ip address


``` sh
ABCHOST=localhost
docker inspect evolution > evolution.json
docker image save evolution -o evolution.tar
ctr -n k8s.io images import evolution.tar
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @evolution.json

```


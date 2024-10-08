# minecraft
![circle_minecraft.svg](icons/circle_minecraft.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](../abcdesktopio/oc.template.ubuntu.gtk)
## Path


``` 
/usr/bin/minecraft-launcher
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
minecraft-launcher.Minecraft Launcher
```

> The WM_CLASS property (of type STRING without control characters) contains two consecutive null-terminated strings. These specify the Instance and Class names to be used by both the client and the window manager for looking up resources for the application or as identifying information.
> to get the WM_CLASS property of an application, use the command line `wmctrl -lx`

## Desktopfile

``` 
/usr/share/applications/minecraft-launcher.desktop
```

> A .desktop file is a simple text file that holds information about a program. It is usually placed in “/usr/share/applications/”.

## PRE run command

> PRE run command are run **before** the package install command

```
RUN apt-get update && apt-get install --no-install-recommends --yes libflite1 openjdk-8-jre at-spi2-core dbus-x11 orca libsecret-1-0 && curl -Ls 'https://launcher.mojang.com/download/Minecraft.deb' -o /tmp/Minecraft.deb && apt-get install --yes /tmp/Minecraft.deb && rm /tmp/Minecraft.deb && rm -rf /var/lib/apt/lists/*
COPY composer/init.d/init.minecraft-launcher /composer/init.d
```



## JSON dump
json source file minecraft.d.3.0.json 

``` json
{
    "acl": {
        "permit": [
            "all"
        ]
    },
    "cat": "games",
    "debpackage": "",
    "icon": "circle_minecraft.svg",
    "keyword": "minecraft",
    "launch": "minecraft-launcher.Minecraft Launcher",
    "name": "minecraft",
    "path": "/usr/bin/minecraft-launcher",
    "rules": {
        "homedir": {
            "default": true
        }
    },
    "template": "abcdesktopio/oc.template.ubuntu.gtk",
    "desktop": "minecraft-launcher.desktop",
    "host_config": {
        "mem_limit": "4G",
        "shm_size": "2G",
        "cpu_period": 200000,
        "cpu_quota": 200000,
        "ipc_mode": "shareable"
    },
    "desktopfile": "/usr/share/applications/minecraft-launcher.desktop",
    "preruncommands": [
        "RUN apt-get update && apt-get install --no-install-recommends --yes libflite1 openjdk-8-jre at-spi2-core dbus-x11 orca libsecret-1-0 && curl -Ls 'https://launcher.mojang.com/download/Minecraft.deb' -o /tmp/Minecraft.deb && apt-get install --yes /tmp/Minecraft.deb && rm /tmp/Minecraft.deb && rm -rf /var/lib/apt/lists/*",
        "COPY composer/init.d/init.minecraft-launcher /composer/init.d"
    ]
}
```

## Install the builded image
>Replace the **ABCHOST** var set to localhost by default to your own server ip address

``` sh
ABCHOST=localhost
curl --output minecraft.d.3.0.json https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/minecraft.d.3.0.json
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @minecraft.d.3.0.json

```

## Generated `DockerFile` source code

``` 
# Dynamic DockerFile application file for abcdesktopio generated by abcdesktopio/oc.apps/make.js
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
ARG TAG=dev
FROM abcdesktopio/oc.template.ubuntu.gtk:$TAG
USER root
RUN apt-get update && apt-get install --no-install-recommends --yes libflite1 openjdk-8-jre at-spi2-core dbus-x11 orca libsecret-1-0 && curl -Ls 'https://launcher.mojang.com/download/Minecraft.deb' -o /tmp/Minecraft.deb && apt-get install --yes /tmp/Minecraft.deb && rm /tmp/Minecraft.deb && rm -rf /var/lib/apt/lists/*
COPY composer/init.d/init.minecraft-launcher /composer/init.d
LABEL oc.icon="circle_minecraft.svg"
LABEL oc.icondata="PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiA8ZGVmcz4KICA8bGluZWFyR3JhZGllbnQgaWQ9ImIiIHgxPSI0MDguMjUiIHgyPSI0MDcuOTQiIHkxPSI1NDcuNiIgeTI9IjQ5OC44OSIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCgxLjMyNzYgMCAwIDEuMzI3NiAtNTEwLjY0IC02NjMuNTIpIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiNmZmYiIG9mZnNldD0iMCIvPgogICA8c3RvcCBzdG9wLWNvbG9yPSIjZTZlNmU2IiBvZmZzZXQ9IjEiLz4KICA8L2xpbmVhckdyYWRpZW50PgogIDxmaWx0ZXIgaWQ9ImQiIHg9Ii0uMDU4ODgzIiB5PSItLjA2MTE2MSIgd2lkdGg9IjEuMTE3OCIgaGVpZ2h0PSIxLjEyMjMiIGNvbG9yLWludGVycG9sYXRpb24tZmlsdGVycz0ic1JHQiI+CiAgIDxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjEwLjU2MjM3OSIvPgogIDwvZmlsdGVyPgogIDxmaWx0ZXIgaWQ9ImMiIHg9Ii0uMDM2IiB5PSItLjAzNiIgd2lkdGg9IjEuMDcyIiBoZWlnaHQ9IjEuMDcyIiBjb2xvci1pbnRlcnBvbGF0aW9uLWZpbHRlcnM9InNSR0IiPgogICA8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIwLjg4OTcyNDQ5Ii8+CiAgPC9maWx0ZXI+CiAgPGZpbHRlciBpZD0iZiIgeD0iLS4wNjQ2NjYiIHk9Ii0uMDU2MDAyIiB3aWR0aD0iMS4xMjkzIiBoZWlnaHQ9IjEuMTEyIiBjb2xvci1pbnRlcnBvbGF0aW9uLWZpbHRlcnM9InNSR0IiPgogICA8ZmVHYXVzc2lhbkJsdXIgc3RkRGV2aWF0aW9uPSIwLjY2MTQ0MzYzIi8+CiAgPC9maWx0ZXI+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJlIiB4MT0iMjUuNjgiIHgyPSIyNi40NDgiIHkxPSIzOS4zOTUiIHkyPSIxNy4zNzYiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KICAgPHN0b3Agc3RvcC1jb2xvcj0iIzM0NWYyOSIgb2Zmc2V0PSIwIi8+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiM1OWE0NDYiIG9mZnNldD0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJhIiB4MT0iMTUuNzA3IiB4Mj0iMjUuNjgiIHkxPSIzMi41NjEiIHkyPSIzOS4zOTUiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KICAgPHN0b3Agc3RvcC1jb2xvcj0iI2FkN2M1OSIgb2Zmc2V0PSIwIi8+CiAgIDxzdG9wIHN0b3AtY29sb3I9IiM4MzViNDEiIG9mZnNldD0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiA8L2RlZnM+CiA8cmVjdCB0cmFuc2Zvcm09Im1hdHJpeCgxLjAxMTUgMCAwIDEuMDExNSAtMzg5LjMyIC00ODkuOTIpIiB4PSIzODYuODUiIHk9IjQ4Ni4zMSIgd2lkdGg9IjU5LjMxNSIgaGVpZ2h0PSI1OS4zMTUiIHJ5PSIyOS42NTciIGZpbHRlcj0idXJsKCNjKSIgb3BhY2l0eT0iLjI1Ii8+CiA8cmVjdCB4PSIxLjk4MjYiIHk9IjEuOTc4NCIgd2lkdGg9IjU5Ljk5NyIgaGVpZ2h0PSI1OS45OTciIHJ5PSIyOS45OTgiIGZpbGw9InVybCgjYikiIHN0cm9rZS13aWR0aD0iMS4wMTE1Ii8+CiA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjMwMzUgMCAwIDEuMzE3IC0xLjQ3NTIgLTYuNTUxMSkiIGZpbHRlcj0idXJsKCNmKSIgb3BhY2l0eT0iLjEiPgogIDxwYXRoIHRyYW5zZm9ybT0ibWF0cml4KDEuMDIyOSAwIDAgMS4wMTI0IC44NzU5OSA0Ljk3NDEpIiBkPSJtMjUgMTEtMTIgN3YxNGwxMiA3IDEyLTd2LTE0eiIgZmlsbC1ydWxlPSJldmVub2RkIi8+CiA8L2c+CiA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjMwMzUgMCAwIDEuMzE3IC0yLjQ3NDcgLTcuODg0MSkiIGZpbGwtcnVsZT0iZXZlbm9kZCI+CiAgPHBhdGggZD0ibTE0LjE3MyAyMy4yIDEyLjI3NSAyMS4yNTcgMTIuMjczLTIxLjI1Ny0xMi4yNzMtNy4wOSIgZmlsbD0idXJsKCNlKSIvPgogIDxwYXRoIGQ9Im0xNC4xNzMgMjMuMnYzLjU0M2wxMi4yNzQgNy4wOSAxZS0zIC0zLjU0N3oiIGZpbGw9IiM1OWE4NDkiLz4KICA8cGF0aCBkPSJtMjYuNDQ4IDMzLjgyNyAxMi4yNzQtNy4wODd2LTMuNTQzbC0xMi4yNzQgNy4wODZ6IiBmaWxsPSIjM2U3MjMxIi8+CiAgPHBhdGggZD0ibTE0LjE3MyAyNi43NHYxMC42M2wxMi4yNzQgNy4wODd2LTEwLjYzeiIgZmlsbD0idXJsKCNhKSIvPgogIDxwYXRoIGQ9Im0yNi40NDggMzMuODI3IDEyLjI3NC03LjA4N3YxMC42M2wtMTIuMjc0IDcuMDg3eiIgZmlsbD0iIzU3M2QyYiIvPgogPC9nPgo8L3N2Zz4K"
LABEL oc.keyword="minecraft,minecraft"
LABEL oc.cat="games"
LABEL oc.desktopfile="minecraft-launcher.desktop"
LABEL oc.launch="minecraft-launcher.Minecraft Launcher"
LABEL oc.template="abcdesktopio/oc.template.ubuntu.gtk"
LABEL oc.name="minecraft"
LABEL oc.displayname="minecraft"
LABEL oc.path="/usr/bin/minecraft-launcher"
LABEL oc.type=app
LABEL oc.rules="{\"homedir\":{\"default\":true}}"
LABEL oc.acl="{\"permit\":[\"all\"]}"
LABEL oc.host_config="{\"mem_limit\":\"4G\",\"shm_size\":\"2G\",\"cpu_period\":200000,\"cpu_quota\":200000,\"ipc_mode\":\"shareable\"}"
RUN for d in /usr/share/icons /usr/share/pixmaps ; do echo "testing link in $d"; if [ -d $d ] && [ -x /composer/safelinks.sh ] ; then echo "fixing link in $d"; cd $d ; /composer/safelinks.sh ; fi; done
ENV APPNAME "minecraft"
ENV APPBIN "/usr/bin/minecraft-launcher"
ENV APP "/usr/bin/minecraft-launcher"
USER root
RUN mkdir -p /var/secrets/abcdesktop/localaccount
RUN for f in passwd shadow group gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /var/secrets/abcdesktop/localaccount; rm -f /etc/$f; ln -s /var/secrets/abcdesktop/localaccount/$f /etc/$f; fi; done
USER balloon
CMD [ "/composer/appli-docker-entrypoint.sh" ]

```

## Rebuild the image manually

### Download the Dockerfile manually
[Dockerfile for application minecraft](https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/minecraft.d)
``` sh
wget https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/minecraft.d
```

### build the `Dockerfile` to create a container image

``` sh
docker build --build-arg TAG=3.0 -f minecraft.d -t minecraft .
```

### Install the new image
>If you are using `containerd` as container runtime, use the ctr command line

 
>If you are not running this bash command on your abcdesktop node
>Replace the **ABCHOST** variable set to localhost by default to your own server ip address


``` sh
ABCHOST=localhost
docker inspect minecraft > minecraft.json
docker image save minecraft -o minecraft.tar
ctr -n k8s.io images import minecraft.tar
curl -X PUT -H 'Content-Type: text/javascript' http://$ABCHOST:30443/API/manager/image -d @minecraft.json

```


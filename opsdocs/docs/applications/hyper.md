# hyper
![hyper.svg](/applications/icons/hyper.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](abcdesktopio/oc.template.ubuntu.minimal.22.04.md)
## Display name
"hyper"
## path
"/opt/Hyper/hyper"
## Mime Type
"x-scheme-handler/ssh"
## Pre run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes libgtk-3-0 libx11-xcb1 libasound2 && apt-get clean,RUN curl -Ls -o /tmp/hyper.deb  https://releases.hyper.is/download/deb && apt-get install  --no-install-recommends --yes /tmp/hyper.deb && apt-get clean && rm -rf /tmp/hyper.deb
```

# whatsdesk
![whatsapp.svg](/applications/icons/whatsapp.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk.20.04](abcdesktopio/oc.template.ubuntu.gtk.20.04.md)
## use ubuntu package
dbus-x11
## Display name
"whatsdesk"
## path
"/opt/whatsdesk/whatsdesk"
## Mime Type
"x-scheme-handler/whatsapp;"
## PRE run command

```

RUN curl -Ls -o /tmp/whatsdesk.deb https://zerkc.gitlab.io/whatsdesk/whatsdesk_0.3.9_amd64.deb,RUN apt-get update && apt-get install --no-install-recommends --yes desktop-file-utils libasound2 && apt-get clean && rm -rf /var/lib/apt/lists/*,RUN apt-get update && apt-get install --no-install-recommends --yes /tmp/whatsdesk.deb && apt-get clean && rm -rf /var/lib/apt/lists/*
```

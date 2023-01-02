# remotedesktopmanager
![circle-remotedesktopmanager.svg](/applications/icons/circle-remotedesktopmanager.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## use ubuntu package
gir1.2-gdkpixbuf-2.0 gtk2-engines-pixbuf libssl3 libgdk-pixbuf2.0-0 adwaita-icon-theme libgdk-pixbuf2.0-bin librsvg2-2 librsvg2-common
## Display name
"RemoteDesktop"
## path
"/bin/remotedesktopmanager.free"
## Pre run command

```

RUN curl -Ls -o /tmp/RemoteDesktopManager.Free_amd64.deb https://cdn.devolutions.net/download/Linux/RDM/2022.1.2.5/RemoteDesktopManager.Free_2022.1.2.5_amd64.deb,RUN apt-get update && apt-get install --yes /tmp/RemoteDesktopManager.Free_amd64.deb && apt-get clean,COPY composer/init.d/init.RemoteDesktopManager.Free /composer/init.d/init.RemoteDesktopManager.Free
```

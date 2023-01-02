# postman
![circle_postman.svg](/applications/icons/circle_postman.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## Display name
"Postman"
## path
"/usr/local/bin/Postman/app/Postman"
## Pre run command

```

RUN apt-get update && apt-get install --no-install-recommends --yes libgtk-3-0 libatk-bridge2.0-0 libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libnss3 qt5dxcb-plugin  libxss1 libasound2 libx11-xcb1 libxcb-dri3-0 libdrm2  libdrm-common libgbm1 libasound2-plugins libgail-common libgtk2.0-bin && apt-get clean,RUN curl -Ls -o /tmp/postman.tar.gz https://dl.pstmn.io/download/latest/linux64 && gunzip -d /tmp/postman.tar.gz && cd /usr/local/bin && tar -xvf /tmp/postman.tar && rm -rf /tmp/blender.tar
```

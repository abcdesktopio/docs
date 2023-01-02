# Brackets
![circle_brackets.svg](/applications/icons/circle_brackets.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk.18.04](abcdesktopio/oc.template.ubuntu.gtk.18.04.md)
## Arguments
"--no-sandbox  --disable-gpu"
## Display name
"Brackets"
## path
"/opt/brackets/Brackets"
## Pre run command

```

RUN curl -Ls -o /tmp/bracket.deb https://github.com/adobe/brackets/releases/download/release-1.14.1/Brackets.Release.1.14.1.64-bit.deb,RUN apt-get update && apt-get install --no-install-recommends --yes libgtk-3-0 libatk-bridge2.0-0 libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 libnss3 qt5dxcb-plugin libxss1 libasound2 libx11-xcb1 libxcb-dri3-0 libdrm2  libdrm-common libgbm1 libasound2-plugins libgail-common libgtk2.0-bin libcurl3 libxss1 && apt-get clean,RUN apt-get update && apt-get install --no-install-recommends --yes /tmp/bracket.deb && rm /tmp/bracket.deb  && apt-get clean && rm -rf /var/lib/apt/lists/*
```

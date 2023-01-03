# beekeeperstudio
![beekeeper-studio.svg](/applications/icons/beekeeper-studio.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## Arguments
"--no-sandbox"
## Display name
"Beekeeper-studio"
## path
"/opt/Beekeeper-Studio/beekeeper-studio"
## File extensions
"sql"
## Legacy file extensions
"sql"
## PRE run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes libxss1 libasound2 libx11-xcb1 libxcb-dri3-0 libdrm2  libdrm-common libgbm1 && apt-get clean,RUN curl -Ls https://deb.beekeeperstudio.io/beekeeper.key | apt-key add -,RUN echo "deb https://deb.beekeeperstudio.io stable main" | tee /etc/apt/sources.list.d/beekeeper-studio-app.list,RUN apt-get update && apt-get install  --no-install-recommends --yes beekeeper-studio libxshmfence1 && apt-get clean,RUN mv "/opt/Beekeeper Studio/" /opt/Beekeeper-Studio,ENV ELECTRON_ENABLE_LOGGING=true,ENV QT_X11_NO_MITSHM=1
```

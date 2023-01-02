# minecraft
![circle_minecraft.svg](/applications/icons/circle_minecraft.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## Display name
"minecraft"
## path
"/usr/bin/minecraft-launcher"
## Pre run command

```

RUN apt-get update && apt-get install --no-install-recommends --yes libflite1 openjdk-8-jre at-spi2-core dbus-x11 orca libsecret-1-0 && curl -Ls 'https://launcher.mojang.com/download/Minecraft.deb' -o /tmp/Minecraft.deb && apt-get install --yes /tmp/Minecraft.deb && rm /tmp/Minecraft.deb && rm -rf /var/lib/apt/lists/*,COPY composer/init.d/init.minecraft-launcher /composer/init.d
```

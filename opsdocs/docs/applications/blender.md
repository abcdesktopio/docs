# blender
![blender.svg](/applications/icons/blender.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk](abcdesktopio/oc.template.gtk.md)
## Display name
"Blender"
## path
"/usr/local/blender-2.90.0-linux64/blender"
## Mime Type
"application/x-blender"
## File extensions
"blend,obj,fbx,3ds,ply,stl"
## Pre run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes xz-utils wget && apt-get clean,RUN apt-get update && apt-get install                          --yes libx11-6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 && apt-get clean,RUN wget -O /tmp/blender.tar.xz https://download.blender.org/release/Blender2.90/blender-2.90.0-linux64.tar.xz && xz -d /tmp/blender.tar.xz && cd /usr/local && tar -xvf /tmp/blender.tar && rm -rf /tmp/blender.tar
```

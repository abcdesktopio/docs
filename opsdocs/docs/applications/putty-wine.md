# putty-wine
![putty.svg](/applications/icons/putty.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.alpine.minimal](abcdesktopio/oc.template.alpine.minimal.md)
## Arguments
"/composer/bin/putty.exe"
## Display name
"Putty Wine (alpine)"
## path
"/usr/bin/wine64"
## Pre run command

```

ENV WINEARCH=win64,RUN mkdir -p /composer/bin,RUN curl -Ls -o /composer/bin/putty.exe https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe
```

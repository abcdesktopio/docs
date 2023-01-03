# winhelp-wine
![winhelp.svg](/applications/icons/winhelp.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.wine](abcdesktopio/oc.template.wine.md)
## Arguments
"winhelp"
## Display name
"Winhelp Wine"
## path
"/usr/bin/wine"
## Mime Type
"application/hlp;"
## File extensions
"hlp;"
## PRE run command

```

ENV WINEARCH=win64,ENV WINEDLLOVERRIDES="mscoree,mshtml=",USER $BUSER,RUN wineboot --init,RUN echo disable > $WINEPREFIX/.update-timestamp,COPY --chown=$BUSER:$BUSER user.reg system.reg /composer/.wine/
```

# winscp-wine
![winscp.svg](/applications/icons/winscp.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.wine](abcdesktopio/oc.template.wine.md)
## Arguments
"/composer/bin/winscp.exe"
## Display name
"WinSCP"
## path
"/usr/bin/wine"
## Pre run command

```

ENV WINEARCH=win64,ENV WINEDLLOVERRIDES="mscoree,mshtml=",USER $BUSER,RUN wineboot --init,RUN curl -Ls -o /tmp/winscp553.zip http://winscp.net/download/winscp553.zip && unzip /tmp/winscp553.zip -d /composer/bin/ && rm /tmp/winscp553.zip,RUN echo disable > $WINEPREFIX/.update-timestamp,COPY --chown=$BUSER:$BUSER user.reg system.reg /composer/.wine/
```

# drawio
![circle_drawio.svg](/applications/icons/circle_drawio.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk.language-pack-all](abcdesktopio/oc.template.ubuntu.gtk.language-pack-all.md)
## Display name
"drawio"
## path
"/opt/drawio/drawio"
## Mime Type
"application/vnd.jgraph.mxfile;application/vnd.visio;"
## File extensions
"drawio"
## Legacy file extensions
"drawio"
## Pre run command

```

RUN apt-get update && curl -Ls 'https://github.com/jgraph/drawio-desktop/releases/download/v20.3.0/drawio-amd64-20.3.0.deb' -o /tmp/drawio-amd64.deb && apt-get install --yes --no-install-recommends /tmp/drawio-amd64.deb && rm /tmp/drawio-amd64.deb && rm -rf /var/lib/apt/lists/*
```

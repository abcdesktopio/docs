# edge
![circle_microsoft-edge.svg](/applications/icons/circle_microsoft-edge.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](abcdesktopio/oc.template.ubuntu.minimal.22.04.md)
## use ubuntu package
fonts-noto fonts-roboto xfonts-100dpi fonts-ubuntu fonts-freefont-ttf fonts-wine
## Arguments
"--no-sandbox --disable-gpu --disable-dev-shm-usage"
## Display name
"MicrosoftEdge"
## path
"/usr/bin/microsoft-edge"
## Mime Type
"application/pdf;application/rdf+xml;application/rss+xml;application/xhtml+xml;application/xhtml_xml;application/xml;image/gif;image/jpeg;image/png;image/webp;text/html;text/xml;x-scheme-handler/http;x-scheme-handler/https;"
## File extensions
"html;xml;gif"
## Legacy file extensions
"html;xml"
## PRE run command

```

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg,RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/edge.list,RUN apt update && apt install -y microsoft-edge-stable && apt-get clean && rm -rf /var/lib/apt/lists/*
```

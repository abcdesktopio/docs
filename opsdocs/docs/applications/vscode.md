# VSCode
![circle_visual-studio-code.svg](/applications/icons/circle_visual-studio-code.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](abcdesktopio/oc.template.ubuntu.minimal.22.04.md)
## Arguments
"--extensions-dir /usr/share/code/extensions --verbose"
## Display name
"VSCode"
## path
"/usr/bin/code"
## Mime Type
"text/x-c;application/json;application/javascript;application/xml;text/xml;application/java-archive;text/x-java-source;text/plain;image/svg+xml;application/x-csh;text/x-yaml;application/x-yaml;application/x-python;"
## File extensions
"c;cpp;py;json;js;java;jav;md;xml;txt;svg;html;htm;sh;csh;css;jsx;tsx;vue;yml;yaml;"
## Legacy file extensions
"c;cpp;py;json;java;md;yml;yaml;"
## PRE run command

```

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg,RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/teams.list,RUN apt update && apt install -y --no-install-recommends code && apt-get clean && rm -rf /var/lib/apt/lists/*
```

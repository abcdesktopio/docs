# teams
![teams.svg](/applications/icons/teams.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](abcdesktopio/oc.template.ubuntu.minimal.22.04.md)
## Arguments
"--disable-namespace-sandbox --disable-setuid-sandbox"
## Display name
"Microsoft Teams"
## path
"/usr/bin/teams"
## Mime Type
"x-scheme-handler/msteams;"
## PRE run command

```

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg,RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/ms-teams stable main" > /etc/apt/sources.list.d/teams.list,RUN apt update && apt install -y teams && apt-get clean && rm -rf /var/lib/apt/lists/*
```

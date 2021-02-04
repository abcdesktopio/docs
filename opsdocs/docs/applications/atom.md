# Atom
![atom.svg](/applications/icons/atom.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk](abcdesktopio/oc.template.gtk.md)
## use ubuntu package
libxss1 atom aspell
## Arguments
"-f"
## Display name
"Atom"
## path
"/usr/bin/atom"
## Pre run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes wget && apt-get clean,RUN apt-get update && apt-get install                          --yes libxss1 && apt-get clean,RUN wget -qO - https://packagecloud.io/AtomEditor/atom/gpgkey | apt-key add -,RUN echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list,RUN apt-get update && apt-get install  --no-install-recommends --yes $(apt-cache search aspell- | awk '{print $1 }') && rm -rf /var/lib/apt/lists/*
```

# corsix-th
![games.svg](/applications/icons/games.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk.language-pack-all](abcdesktopio/oc.template.ubuntu.gtk.language-pack-all.md)
## use ubuntu package
libgl1 corsix-th
## Display name
"corsix-th"
## path
"/usr/games/corsix-th"
## Pre run command

```

RUN apt-get update && apt-get install --no-install-recommends --yes unzip && apt-get clean,RUN cd /composer &&  curl -Ls https://th.corsix.org/Demo.zip -o Demo.zip && unzip Demo.zip && rm -rf Demo.zip,COPY corsix-th.config.txt /composer/corsix-th.config.txt
```

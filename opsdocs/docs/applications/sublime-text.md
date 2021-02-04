# Sublime-Text
![sublime_text.svg](/applications/icons/sublime_text.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk](abcdesktopio/oc.template.gtk.md)
## use ubuntu package
sublime-text
## Display name
"Sublime-Text"
## path
"/opt/sublime_text/sublime_text"
## Pre run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes wget && apt-get clean,RUN wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add -a,RUN echo "deb https://download.sublimetext.com/ apt/stable/" | tee /etc/apt/sources.list.d/sublime-text.list
```

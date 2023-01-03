# sublime-Text
![circle_sublime-text.svg](/applications/icons/circle_sublime-text.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## use ubuntu package
sublime-text
## Display name
"sublime-Text"
## path
"/opt/sublime_text/sublime_text"
## PRE run command

```

RUN curl -Ls https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add -a,RUN echo "deb https://download.sublimetext.com/ apt/stable/" | tee /etc/apt/sources.list.d/sublime-text.list,RUN apt-get update && apt-get install --yes libgl1 && apt-get clean
```

# openshift
![openshift.svg](/applications/icons/openshift.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## use ubuntu package
rhc gnome-terminal
## Arguments
"--disable-factory --class openshift.cli"
## Display name
"OpenShift cli"
## path
"/usr/bin/gnome-terminal"
## PRE run command

```

RUN cd /tmp && wget "https://cli.run.pivotal.io/stable?release=linux64-binary" -O pivotal.tgz && tar -xvf pivotal.tgz && mv cf /usr/local/bin
```

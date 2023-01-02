# cntlm
![cntlm.svg](/applications/icons/cntlm.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](abcdesktopio/oc.template.ubuntu.minimal.22.04.md)
## use ubuntu package
ruby-mustache gnome-terminal dbus-x11 cntlm net-tools vim curl wget
## Arguments
"--class cntlm -- bash -c '/usr/sbin/cntlm -f -v; exec bash'"
## Display name
"cntlm"
## path
"/usr/bin/gnome-terminal"
## Pre run command

```

COPY cntlm/cntlm.mustache  cntlm/init.cntlm.sh /composer/,COPY composer/init.d/init.gnome-terminal /composer/init.d/
```

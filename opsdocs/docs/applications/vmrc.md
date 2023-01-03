# vmrc
![circle_vmware.svg](/applications/icons/circle_vmware.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## Display name
"VMRC"
## path
"/usr/bin/vmrc"
## Mime Type
"x-scheme-handler/vmrc;"
## PRE run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes libaio1 && apt-get clean,COPY VMware-Remote-Console-12.0.1-18113358.x86_64.bundle /tmp,RUN chmod o+x /tmp/VMware-Remote-Console-12.0.1-18113358.x86_64.bundle,RUN /tmp/VMware-Remote-Console-12.0.1-18113358.x86_64.bundle --eulas-agreed --console --required --ignore-errors
```

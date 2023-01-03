# apachedirectorystudio
![account.svg](/applications/icons/account.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.22.04](abcdesktopio/oc.template.ubuntu.22.04.md)
## use ubuntu package
openjdk-11-jre libswt-gtk-4-jni libswt-webkit-gtk-4-jni libswt-cairo-gtk-4-jni libswt-gtk-4-java
## Arguments
"-configuration .eclipse/1988419495_linux_gtk_x86_64"
## Display name
"Apache Directory Studio"
## path
"/usr/local/ApacheDirectoryStudio/ApacheDirectoryStudio"
## PRE run command

```

RUN curl -sL --output /tmp/ApacheDirectoryStudio.tar.gz https://dlcdn.apache.org/directory/studio/2.0.0.v20210717-M17/ApacheDirectoryStudio-2.0.0.v20210717-M17-linux.gtk.x86_64.tar.gz && cd /usr/local && tar -xvf /tmp/ApacheDirectoryStudio.tar.gz && rm -rf /tmp/ApacheDirectoryStudio.tar.gz,RUN mkdir /.ApacheDirectoryStudio && chmod 777 /.ApacheDirectoryStudio,COPY composer/init.d/init.ApacheDirectoryStudio /composer/init.d/
```

# nautilus
![circle_filemanager.svg](/applications/icons/circle_filemanager.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk](abcdesktopio/oc.template.ubuntu.gtk.md)
## use ubuntu package
dbus gnome-icon-theme gnome-icon-theme-symbolic numix-gtk-theme numix-icon-theme gnome-font-viewer dbus-x11 python3-nautilus python3-shellescape nautilus desktop-file-utils shared-mime-info xdg-user-dirs
## Display name
"FileManager"
## path
"/usr/bin/nautilus"
## showinview
"dock"
## PRE run command

```

RUN mkdir -p /run/user/4096 /var/run/dbus/ chown balloon:balloon /run/user/4096 /var/run/dbus,COPY composer/node /composer/node,RUN cd /composer/node/ocdownload && npm install,COPY composer/init.d/init.nautilus /composer/init.d/init.nautilus,COPY composer/desktop_download.py /composer/desktop_download.py,ENV NAUTILUS_PYTHON_DEBUG=misc
```

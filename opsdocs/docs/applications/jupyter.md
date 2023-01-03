# jupyter
![jupyter.svg](/applications/icons/jupyter.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.20.04](abcdesktopio/oc.template.ubuntu.minimal.20.04.md)
## use ubuntu package
gnome-terminal openssh-client telnet netcat sshcommand sshfs ftp-ssl wput curl wget tftp ncftp git git-ftp ftp dbus-x11
## Arguments
"--disable-factory  --class=jupyter -- /usr/local/bin/startjupyter.sh"
## Display name
"jupyter"
## path
"/usr/bin/gnome-terminal"
## showinview
"dock"
## PRE run command

```

RUN add-apt-repository ppa:mozillateam/ppa,COPY etc/apt/preferences.d/mozilla-firefox /etc/apt/preferences.d/mozilla-firefox,RUN apt-get update && apt-get install --no-install-recommends --yes firefox && apt-get clean,RUN apt-get update && apt-get install --no-install-recommends --yes sudo && apt-get clean,RUN apt-get update && apt-get install --no-install-recommends --yes build-essential python3.9 python3-pip python-is-python3 curl libcurl4-openssl-dev libssl-dev firefox wget && apt-get clean,RUN pip3 install torch,RUN pip3 install jupyterlab,RUN pip install jupyterlab-nvdashboard,RUN # jupyter labextension install jupyterlab-nvdashboard
```
## POST run command

```

undefined
```

# jupyternvidia
![jupyter.svg](/applications/icons/jupyter.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.nvidia.22.04](abcdesktopio/oc.template.ubuntu.nvidia.22.04.md)
## use ubuntu package
gnome-terminal openssh-client telnet netcat sshcommand sshfs ftp-ssl wput curl wget tftp ncftp git git-ftp ftp dbus-x11
## Arguments
"--disable-factory  --class=jupyternvidia -- /usr/local/bin/startjupyter.sh"
## Display name
"jupyter nvidia"
## path
"/usr/bin/gnome-terminal"
## showinview
"dock"
## Pre run command

```

RUN add-apt-repository ppa:mozillateam/ppa,COPY etc/apt/preferences.d/mozilla-firefox /etc/apt/preferences.d/mozilla-firefox,RUN apt-get update && apt-get install --no-install-recommends --yes firefox wget sudo && apt-get clean,COPY cudnn-local-repo-ubuntu2204-8.7.0.84_1.0-1_amd64.deb /tmp,RUN apt-get update && apt-get install --no-install-recommends --yes -f /tmp/cudnn-local-repo-ubuntu2204-8.7.0.84_1.0-1_amd64.deb && apt-get clean,RUN cp /var/cudnn-local-repo-ubuntu2204-8.7.0.84/cudnn-local-BF23AD8A-keyring.gpg /usr/share/keyrings/,ENV PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin,ENV LD_LIBRARY_PATH=/usr/local/cuda-12.0/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64,RUN apt-get update && apt-get install --no-install-recommends --yes build-essential python3.9 python3-pip python-is-python3 libcurl4-openssl-dev libssl-dev wget && apt-get clean,RUN # wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh -O /tmp/anaconda3.sh && bash /tmp/anaconda3.sh -b -p /usr/local/anaconda,RUN pip3 install torch,RUN pip3 install tensorflow-gpu,RUN pip3 install jupyter notebook,RUN pip3 install jupyterlab,RUN pip3 install jupyterlab-nvdashboard,RUN # jupyter labextension install jupyterlab-nvdashboard
```

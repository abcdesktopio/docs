# firefox-esr
![firefox.svg](/applications/icons/firefox.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.18.04](abcdesktopio/oc.template.ubuntu.minimal.18.04.md)
## Arguments
"-new-instance -P abcdesktop-firefox-esr --class firefox-esr"
## Display name
"Firefox-esr"
## path
"/usr/bin/firefox-esr"
## showinview
"dock"
## Mime Type
"text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;video/webm;application/x-xpinstall;"
## File extensions
"htm;html;xml;gif"
## Legacy file extensions
"htm;html;xml"
## Pre run command

```

RUN add-apt-repository -y ppa:mozillateam/ppa,RUN DEBIAN_FRONTEND=noninteractive echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections,RUN apt-get update && apt-get install  --no-install-recommends --yes ttf-mscorefonts-installer ttf-bitstream-vera ttf-dejavu ttf-xfree86-nonfree,RUN apt-get update && apt-get install  --no-install-recommends --yes winbind && apt-get clean,RUN apt-get update && apt-get install  --no-install-recommends --yes libasound2-plugins libgail-common libgtk2.0-bin chromium-codecs-ffmpeg-extra gstreamer1.0-libav gstreamer1.0-plugins-ugly gstreamer1.0-vaapi libavcodec-extra && apt-get clean,COPY composer/init.d/init.firefox-esr /composer/init.d/init.firefox-esr,COPY policies.json /usr/lib/firefox-esr/distribution,RUN mkdir -p /etc/adobe,COPY mms.cfg /etc/adobe/mms.cfg,COPY /ntlm_auth /usr/bin/ntlm_auth.desktop,RUN chown root:root /usr/bin/ntlm_auth.desktop && chmod 111 /usr/bin/ntlm_auth.desktop
```

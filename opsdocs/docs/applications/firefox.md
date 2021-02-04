# Firefox
![firefox.svg](/applications/icons/firefox.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk](abcdesktopio/oc.template.gtk.md)
## Display name
"Firefox"
## path
"/usr/bin/firefox"
## showinview
"dock"
## Mime Type
"text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;video/webm;application/x-xpinstall;"
## File extensions
"htm;html;xml;gif"
## Legacy file extensions
"htm;html;xml"
## Share size
"2gb"
## Memory size
"16gb"
## Pre run command

```

RUN DEBIAN_FRONTEND=noninteractive echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections,RUN apt-get update && apt-get install  --no-install-recommends --yes ttf-mscorefonts-installer ttf-bitstream-vera ttf-dejavu ttf-xfree86-nonfree && apt-get clean,RUN apt-get update && apt-get install  --no-install-recommends --yes winbind firefox $(apt-cache search firefox-locale | awk '{print $1 }') && apt-get clean,RUN apt-get update && apt-get install  --no-install-recommends --yes flashplugin-installer ubuntu-restricted-extras libavc1394-0 && apt-get clean,RUN apt-get update && apt-get install  --no-install-recommends --yes libasound2-plugins libgail-common libgtk2.0-bin chromium-codecs-ffmpeg-extra gstreamer1.0-libav gstreamer1.0-plugins-ugly gstreamer1.0-vaapi libavcodec-extra && apt-get clean,COPY composer/init.d/init.firefox /composer/init.d/init.firefox,COPY policies.json /usr/lib/firefox/distribution,COPY /ntlm_auth /usr/bin/ntlm_auth.desktop,RUN chown root:root /usr/bin/ntlm_auth.desktop && chmod 111 /usr/bin/ntlm_auth.desktop,ENV NSS_SDB_USE_CACHE=yes
```

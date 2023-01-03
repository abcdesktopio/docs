# Firefox
![circle_firefox.svg](/applications/icons/circle_firefox.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.gtk.20.04](abcdesktopio/oc.template.ubuntu.gtk.20.04.md)
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
## PRE run command

```

RUN apt-get update && apt-get install --yes krb5-user winbind firefox $(apt-cache search firefox-locale | awk '{print $1 }') && apt-get clean,COPY composer/init.d/init.firefox /composer/init.d/init.firefox,COPY policies.json /usr/lib/firefox/distribution,COPY /ntlm_auth /usr/bin/ntlm_auth.desktop,RUN chown root:root /usr/bin/ntlm_auth.desktop && chmod 111 /usr/bin/ntlm_auth.desktop
```

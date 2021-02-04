# youtube
![youtube.svg](/applications/icons/youtube.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk](abcdesktopio/oc.template.gtk.md)
## use ubuntu package
firefox
## Arguments
"-P youtube --class=youtube https://www.youtube.com/"
## Display name
"Youtube"
## path
"/usr/bin/firefox"
## Mime Type
"text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;video/webm;application/x-xpinstall;"
## File extensions
"html;xml;gif"
## Legacy file extensions
"html;xml"
## Pre run command

```

COPY composer/init.d/init.firefox.youtube /composer/init.d/init.firefox
```

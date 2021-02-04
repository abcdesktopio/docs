# FirefoxRest
![rest.svg](/applications/icons/rest.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk.firefox.rest](abcdesktopio/oc.template.gtk.firefox.rest.md)
## use ubuntu package
firefox winbind
## Arguments
"--class=Rest.Firefox"
## Display name
"Firefox-Rest"
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

COPY composer/init.d/init.firefox /composer/init.d/init.firefox
```

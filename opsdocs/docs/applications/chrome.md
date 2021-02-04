# chrome
![google-chrome.svg](/applications/icons/google-chrome.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk](abcdesktopio/oc.template.gtk.md)
## use ubuntu package
google-chrome-stable
## Arguments
"-no-sandbox --disable-gpu"
## Display name
"Chrome"
## path
"/usr/bin/google-chrome-stable"
## Mime Type
"text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;video/webm;"
## File extensions
"html;xml;gif"
## Legacy file extensions
"html;xml"
## Share size
"2gb"
## Pre run command

```

RUN apt-get update && apt-get install  --no-install-recommends --yes  wget  && apt-get clean,RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -,RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
```

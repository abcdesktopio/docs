# chrome
![circle_google-chrome.svg](/applications/icons/circle_google-chrome.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.ubuntu.minimal.22.04](abcdesktopio/oc.template.ubuntu.minimal.22.04.md)
## use ubuntu package
krb5-user fonts-noto fonts-roboto xfonts-100dpi fonts-ubuntu fonts-freefont-ttf dbus-x11 fonts-wine fonts-recommended google-chrome-stable
## Arguments
"--no-sandbox --disable-gpu --disable-dev-shm-usage"
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
## Pre run command

```

RUN curl -Ls https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -,RUN echo "deb [arch=$(dpkg --print-architecture)] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list
```

# remarkable
![remarkable.svg](/applications/icons/remarkable.svg){: style="height:64px;width:64px"}
## inherite from
[abcdesktopio/oc.template.gtk.18.04](abcdesktopio/oc.template.gtk.18.04.md)
## Display name
"Remarkable"
## path
"/usr/bin/remarkable"
## showinview
"dock"
## Mime Type
"text/x-markdown;text/markdown;"
## File extensions
"md;markdown"
## Legacy file extensions
"md;markdown"
## Pre run command

```

RUN apt-get update && apt-get install --no-install-recommends --yes wget python3-gtkspellcheck wkhtmltopdf python3-markdown gir1.2-gtksource-3.0 yelp gir1.2-webkit-3.0 python3-bs4 && apt-get clean,RUN wget -O /tmp/remarkable_1.87_all.deb https://remarkableapp.github.io/files/remarkable_1.87_all.deb && dpkg -i /tmp/remarkable_1.87_all.deb && rm -rf /tmp/remarkable_1.87_all.deb
```

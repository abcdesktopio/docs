# Application image format

abcdesktop.io uses OCI container image format and add some labels to describe the application.
Labels add metadata to the container image.

## Requirements

- A running container enegine (like dockerd) 
- An access to the docker public registry

## Labels

Docker images applications for abcdesktop use docker's LABELS as metadata. To select only abcdesktop applications from standard docker images, all abcdesktop's applications must have a label 'oc.type' set to the value 'app'.

```Dockerfile
LABEL oc.type=app
```

### Label descriptions

| Label name                       | Type     | Description                                                                                | Sample |
|----------------------------------|--------- |--------------------------------------------------------------------------------------------|--------|
|  ```oc.icon```                   | string   | icon filename use by the web interface for the application, **MUST suffix in .svg** format |writer.svg | 
|  ```oc.icondata```               | string   | icon file **SVG data uuencoded**                                                           | PD94b...C9zdmc+Cg== | 
|  ```oc.keyword```                | string   | keywords use by the web application search engine separated by comma(,)                                         | firefox,mozilla,web,internet | 
|  ```oc.desktopfile```            | string   | .desktop gnome file name                 | /usr/share/applications/firefox.desktop | 
|  ```oc.cat```                    | string   | category use by the web application store, choose one value of the default list ```[ 'office', 'games', 'graphics', 'development', 'utilities', 'education'  ]```               | office | 
|  ```oc.launch```                 | string   | **X11 Windows Class name**. It MUST be unique use the command 'wmctrl -lx' to can the right name |  | 
|  ```oc.template```               | string   | Template name to use FROM in the DockerFile              | oc.template.gtk.firefox | 
|  ```oc.path```                   | string   | Path to the application binary | /usr/bin/firefox |
|  ```oc.args```                   | string   | arguments added to the command | --open | 
|  ```oc.name```                   | string   | Name of the application              | Firefox | 
|  ```oc.displayname```            | string   | Display Name show by Web interface              | Firefox | 
|  ```oc.type```                   | string   | Always set to the value 'app'              | app | 
|  ```oc.mimetype```               | string   | MimeType supported by the application separated by semicolon(;) | text/html;text/xml;application/xml;application/rss+xml;video/webm  | 
|  ```oc.showinview```             | string   | Set to the dock to add this app in dock              | dock | 
|  ```oc.fileextensions```         | string   | Supported extensions file, separated by semicolon(;) | htm;html;xml;gif  | 
|  ```oc.legacyfileextensions```   | string   | Legacy file extensions, separated by semicolon(;)    | htm;html;xml      | 
|  ```oc.host_config```            | dict   | dictionary of resources (see resources details)     |  { 'shm_size': '1g' }   | 



Example for Firefox application

```
LABEL oc.icon="firefox.svg"
LABEL oc.keyword="firefox,mozilla,internet"
LABEL oc.cat="office"
LABEL oc.launch="Navigator.Firefox"
LABEL oc.template="oc.template.gtk.firefox"
LABEL oc.name="Firefox"
LABEL oc.displayname="Firefox"
LABEL oc.path="/usr/bin/firefox"
LABEL oc.type=app
LABEL oc.showinview="dock"
LABEL oc.mimetype="text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml"
LABEL oc.fileextensions="html;xml;gif"
LABEL oc.legacyfileextensions="html;xml"
```
 
## host_config resource description

`host_config` resource description allows to change the running context for docker application.
`host_config` is a dictionary and uses the same format in `applist.json` file and `od.config` file.

For example you can set low cpu and memory values to an application like the great X11 xeyes.

```json
{ 	
	"mem_limit":  "32M", 
	"cpu_period":  50000, 
	"cpu_quota":   50000, 
	"pid_mode":   false, 
	"network_mode": "none" 
}
```

Read the dedicated chapter for resource description, to get more informations on [host_config](/config/host_config/)
 

## Inspect an abcdesktop docker images

To download an abcdesktop docker image, run the command

```
docker pull abcdesktopio/firefox.d
```

To inspect the labels in the docker image, run docker inspect

```
docker inspect abcdesktopio/firefox.d:latest
```

Read the labels section :

```
"Labels": {
                "architecture": "x86_64",
                "oc.cat": "office",
                "oc.desktopfile": "firefox.desktop",
                "oc.displayname": "Firefox",
                "oc.fileextensions": "htm;html;xml;gif",
                "oc.icon": "firefox.svg",
                "oc.icondata": "PD94b.. CUT HERE ...C9zdmc+Cg==",
                "oc.keyword": "firefox,mozilla,web,internet",
                "oc.launch": "Navigator.Firefox",
                "oc.legacyfileextensions": "htm;html;xml",
                "oc.mimetype": "text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;video/webm;application/x-xpinstall;",
                "oc.name": "Firefox",
                "oc.path": "/usr/bin/firefox",
                "oc.showinview": "dock",
                "oc.template": "oc.template.gtk.firefox",
                "oc.type": "app",
                "oc.usedefaultapplication": "true",
                "release": "5",
                "vcs-ref": "master",
                "vcs-type": "git",
                "version": "1.2"
 }
```

 
 

## The inheritance of the images

All abcdesktop applications use by default the oc.template.gtk images name. 

### The inheritance of the classes. 

By default, ```oc.templace.gtk``` is the main image for all applications. 
For example ```oc.template.gtk.firefox``` use the ```oc.template.gtk``` image. ```oc.template.gtk.firefox.acme``` use the ```oc.template.gtk.firefox```.  

- The ```oc.template.gtk.firefox``` contains the Mozilla Firefox application.
- The ```oc.template.gtk.firefox.acme``` may contain custom set for Mozilla Firefox application, like Root CA, proxy values or policy.json files for the acme.

```
+------------------------------+
|oc.template.gtk.firefox.acme  |
+---------------+--------------+
                |
                |
+---------------+--------------+
|oc.template.gtk.firefox       |
+---------------+--------------+
                |
                |
+---------------+--------------+
|oc.template.gtk               |
+---------------+--------------+
```

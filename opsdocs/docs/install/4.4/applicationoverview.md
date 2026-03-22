# Applications


## Application description

An application for abcdesktop is a simple [OCI](https://github.com/opencontainers/image-spec) JSON file. A docker inspect command line dumps the JSON file content.

```
  docker inspect $YOUR_IMAGE_NAME 
```

The image must contains some labels, for example.

```
LABEL oc.icon="firefox.svg"
LABEL oc.keyword="firefox,mozilla,internet"
LABEL oc.cat="office"
LABEL oc.launch="Navigator.Firefox"
LABEL oc.name="Firefox"
LABEL oc.path="/usr/bin/firefox"
LABEL oc.type=app
```
 
## Install an application 

To install an application for abcdesktop, you can 
- use the install [bash script](bash.md)
- use the [Web UI console](applicationwithconsole.md)
- run a curl command line to PUT the JSON file to API service

```
curl 
```


# abcdesktop a simple application `xedit`

## Release 3.4

Release `3.4` add a simple application support 

## Requirements

You need to have a 

- kubernetes cluster ready to run whith abcdesktop.io installed
- `kubectl` or `microk8s` command-line tool must be configured to communicate with your cluster. 
- `docker` command line must be installed too.
- your own registry


## Create a simple application `xedit`


To illustrate a simple application, we will install `X11/xedit` inside a container. 

* Create a Dockerfile to install `xedit` application from `x11-apps` package

```Dockerfile
FROM ubuntu
RUN apt-get update && apt-get install -y --no-install-recommends x11-apps && apt-get clean
LABEL oc.launch=xedit.Xedit
RUN mkdir -p /etc/localaccount 
RUN for f in passwd shadow group gshadow ; do if [ -f /etc/$f ] ; then  cp /etc/$f /etc/localaccount; rm -f /etc/$f; ln -s /etc/localaccount/$f /etc/$f; fi; done
CMD ["/usr/bin/xedit"]
```

Dockerfile description 

This image is based on ubuntu, and install the `x11-apps` package. Then we define `/usr/bin/xedit` as the CMD, ENTRYPOINT is also supported.

* `oc.launch` label is the name of the X11 window's `WM_CLASS`
- create a directory `/etc/localaccount`
- the execute runtime adds the generated files [ `passwd`, `shadow`, `group`, `gshadow` ] to the current container in `/etc/localaccount`


* Build the image for xedit application

```bash
REGISTRY=abcdesktopio
docker build -t $REGISTRY/samplexedit .
```

> You should replace the value of `REGISTRY=abcdesktopio` by your own registry's name.
If you don't have one, you can use the `abcdesktopio/samplexedit` as a readonly dockerhub registry.


* Push the image to your registry *(only if you have your own registry)*

```bash
REGISTRY=abcdesktopio
docker push $REGISTRY/samplexedit
```

* Inspect the image to create a json file

```bash
REGISTRY=abcdesktopio
docker inspect $REGISTRY/samplexedit:latest > samplexedit.json
```

* Send the image to abcdesktop pyos instance

The commands read the `PYOS_POD` name, then copy the `samplexeyes.json` file to `/tmp` of PYOS_POD,
then send the `/tmp/samplexeyes.json` to REST API server

```bash
NAMESPACE=abcdesktop
PYOS_POD_NAME=$(kubectl get pods -l run=pyos-od -o jsonpath={.items..metadata.name} -n "$NAMESPACE" | awk '{print $1}')
kubectl cp samplexeyes.json $PYOS_POD_NAME:/tmp -n $NAMESPACE
kubectl exec -i $PYOS_POD_NAME -n abcdesktop -- curl -X POST -H 'Content-Type: text/javascript' http://localhost:8000/API/manager/image -d @/tmp/samplexedit.json
```

The endpoint image returns a json documment 

```json
[
  {
    "cmd": [
      "/usr/bin/xedit"
    ],
    "path": null,
    "sha_id": "sha256:271cbe5516574119905fe83a733dc5f1c46c1ea337e3e888de63ed419f7e7186",
    "id": "abcdesktopio/samplexedit:latest",
    "architecture": "amd64",
    "os": "linux",
    "rules": {},
    "acl": {
      "permit": [
        "all"
      ]
    },
    "launch": "xedit.Xedit",
    "name": "xedit",
    "icon": "xedit",
    "icondata": "PHN2ZyB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCA2NCA2NCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0id2hpdGUiLz48dGV4dCB4PSIwIiB5PSIzMiIgZmlsbD0iYmxhY2siPnhlZGl0PC90ZXh0Pjwvc3ZnPg==",
    "keyword": null,
    "uniquerunkey": null,
    "cat": null,
    "args": null,
    "execmode": null,
    "showinview": null,
    "displayname": "xedit",
    "desktopfile": null,
    "executeclassname": null,
    "executablefilename": "xedit",
    "usedefaultapplication": false,
    "mimetype": [],
    "fileextensions": [],
    "legacyfileextensions": [],
    "secrets_requirement": null,
    "image_pull_policy": "IfNotPresent",
    "image_pull_secrets": null,
    "containerengine": "ephemeral_container",
    "securitycontext": {},
    "created": "2025-02-04T09:36:19.796314327Z"
  }
]
```


## Execute the new application `xedit`

* Open your web browser, and to go your own abcdesktop url, and do a login to create a desktop 

![login to create a desktop](img/simplestapplication-login-xedit.png)

* Look for the new application `xedit` pushed

![Look for the new application xeyes](img/simplestapplication-lookfor-xedit.png)

* Start the new application `xedit`

![Start the new application xeyes](img/simplestapplication-xedit-started.png)


* Save file to check the access list permissions

![SAve new file in the new application xedit](img/simplestapplication-xedit-running.png)

> you can close and start xedit again, to reload you saved file
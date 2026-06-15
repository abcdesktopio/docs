---
tags:
  - application
---

# Build a sample xedit with icon from scratch

Goal: Build and register a new X11 application container (`xedit`) with a custom icon in an abcdesktop.io instance.


## Requirements

You need to have:

- A Kubernetes cluster with abcdesktop.io installed and running.
- `kubectl` or `microk8s` configured to communicate with your cluster.
- `docker` command-line tool installed.
- Your own public or private container registry.


## Create a simple application `xedit`


To illustrate a simple application integration, we will install `xedit` from the `x11-apps` package inside a container image.

* Create a Dockerfile to install the `xedit` application from the `x11-apps` package

```Dockerfile
FROM ubuntu
RUN apt-get update && apt-get install -y --no-install-recommends x11-apps && apt-get clean
LABEL oc.launch=xedit.Xedit
LABEL oc.icon=pencil.svg
LABEL oc.icondata="PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgZmlsbD0iY3VycmVudENvbG9yIiBjbGFzcz0iYmkgYmktcGVuY2lsIiB2aWV3Qm94PSIwIDAgMTYgMTYiPgogIDxwYXRoIGQ9Ik0
xMi4xNDYuMTQ2YS41LjUgMCAwIDEgLjcwOCAwbDMgM2EuNS41IDAgMCAxIDAgLjcwOGwtMTAgMTBhLjUuNSAwIDAgMS0uMTY4LjExbC01IDJhLjUuNSAwIDAgMS0uNjUtLjY1bDItNWEuNS41IDAgMCAxIC4xMS0uMTY4ek0xMS4yMDcgMi41IDEzLjUgNC43OTMgMTQuN
zkzIDMuNSAxMi41IDEuMjA3em0xLjU4NiAzTDEwLjUgMy4yMDcgNCA5LjcwN1YxMGguNWEuNS41IDAgMCAxIC41LjV2LjVoLjVhLjUuNSAwIDAgMSAuNS41di41aC4yOTN6bS05Ljc2MSA1LjE3NS0uMTA2LjEwNi0xLjUyOCAzLjgyMSAzLjgyMS0xLjUyOC4xMDYtLjE
wNkEuNS41IDAgMCAxIDUgMTIuNVYxMmgtLjVhLjUuNSAwIDAgMS0uNS0uNVYxMWgtLjVhLjUuNSAwIDAgMS0uNDY4LS4zMjUiLz4KPC9zdmc+"
CMD ["/usr/bin/xedit"]
```

> oc.icondata is a base64 encoded content of the file `pencil.svg`
![pencil.svg](https://icons.getbootstrap.com/assets/icons/pencil.svg)
> to get it
>```
wget https://icons.getbootstrap.com/assets/icons/pencil.svg && base64 -w0 pencil.svg
```

**Dockerfile description**

This image is based on Ubuntu and installs the `x11-apps` package. The default command is set to `/usr/bin/xedit` via the `CMD` instruction. `ENTRYPOINT` is also supported.

* `oc.launch` label is the name of the X11 window's `WM_CLASS`
* `oc.icon` is the name of the icon file
* `oc.icondata` is a base64 encoded content of the file `pencil.svg`
![pencil.svg](https://icons.getbootstrap.com/assets/icons/pencil.svg) to get it
`wget https://icons.getbootstrap.com/assets/icons/pencil.svg && base64 -w0 pencil.svg`

* Build the image for the xedit application

```bash
REGISTRY=abcdesktopio
docker build -t $REGISTRY/samplexedit .
```

> Replace the value of `REGISTRY=abcdesktopio` with your own registry name.
> If you do not have one, you can use `abcdesktopio/samplexedit` as a read-only Docker Hub registry.


* Push the image to your registry *(only if you have your own registry)*

```bash
REGISTRY=abcdesktopio
docker push $REGISTRY/samplexedit
```

* Inspect the image to create a JSON file

```bash
REGISTRY=abcdesktopio
docker inspect $REGISTRY/samplexedit > samplexedit.json
```

* Send the image to the abcdesktop pyos instance

The following commands retrieve the `PYOS_POD` name, copy the `samplexedit.json` file to the `/tmp` directory inside the pyos pod, and submit the file to the REST API server.

```bash
NAMESPACE=abcdesktop
PYOS_POD_NAME=$(kubectl get pods -l run=pyos-od -o jsonpath={.items..metadata.name} -n "$NAMESPACE" | awk '{print $1}')
kubectl cp samplexedit.json $PYOS_POD_NAME:/tmp -n $NAMESPACE
kubectl exec -i $PYOS_POD_NAME -n abcdesktop -- curl -X POST -H 'Content-Type: text/javascript' http://localhost:8000/API/manager/image -d @/tmp/samplexedit.json
```

The image endpoint returns a JSON document

```json
[
  {
    "cmd": [
      "/usr/bin/xedit"
    ],
    "path": null,
    "sha_id": "sha256:bf33c7ad1e6b7205f5b8117f2b8f00455a4b9aa1575ec67064a9d96820df71ba",
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
    "wm_class": null,
    "name": "xedit",
    "icon": "pencil.svg",
    "icondata": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgZmlsbD0iY3VycmVudENvbG9yIiBjbGFzcz0iYmkgYmktcGVuY2lsIiB2aWV3Qm94PSIwIDAgMTYgMTYiPgogIDxwYXRoIGQ9Ik0xMi4xNDYuMTQ2YS41LjUgMCAwIDEgLjcwOCAwbDMgM2EuNS41IDAgMCAxIDAgLjcwOGwtMTAgMTBhLjUuNSAwIDAgMS0uMTY4LjExbC01IDJhLjUuNSAwIDAgMS0uNjUtLjY1bDItNWEuNS41IDAgMCAxIC4xMS0uMTY4ek0xMS4yMDcgMi41IDEzLjUgNC43OTMgMTQuNzkzIDMuNSAxMi41IDEuMjA3em0xLjU4NiAzTDEwLjUgMy4yMDcgNCA5LjcwN1YxMGguNWEuNS41IDAgMCAxIC41LjV2LjVoLjVhLjUuNSAwIDAgMSAuNS41di41aC4yOTN6bS05Ljc2MSA1LjE3NS0uMTA2LjEwNi0xLjUyOCAzLjgyMSAzLjgyMS0xLjUyOC4xMDYtLjEwNkEuNS41IDAgMCAxIDUgMTIuNVYxMmgtLjVhLjUuNSAwIDAgMS0uNS0uNVYxMWgtLjVhLjUuNSAwIDAgMS0uNDY4LS4zMjUiLz4KPC9zdmc+",
    "keyword": null,
    "uniquerunkey": null,
    "cat": null,
    "args": null,
    "execmode": null,
    "showinview": null,
    "displayname": "xedit",
    "desktopfile": null,
    "executeclassname": null,
    "runtimeClassName": null,
    "executablefilename": "xedit",
    "usedefaultapplication": false,
    "mimetype": [],
    "fileextensions": [],
    "legacyfileextensions": [],
    "secrets_requirement": null,
    "containerengine": "ephemeral_container",
    "securitycontext": {},
    "created": "2026-04-06T14:40:03.26147483+02:00"
  }
]
```


## Execute the new application `xedit`

* Open your web browser, navigate to your abcdesktop URL, and log in to create a desktop

![login to create a desktop](img/simplestapplication-login-xedit.png)

* Search for the newly registered `xedit` application

![Look for the new application xedit](img/simplestapplication-lookfor-xedit.png)

* Launch the `xedit` application

The `xedit` container image is being pulled.

![Start the new application xedit](img/simplestapplication-xedit-starting.png)

The `xedit` container image is starting.

![Start the new application xedit](img/simplestapplication-xedit-started.png)

The `xedit` application is running.


You have successfully installed the `xedit` application as a container with a custom icon.


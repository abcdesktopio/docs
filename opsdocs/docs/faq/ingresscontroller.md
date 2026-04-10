---
tags:
  - faq
  - ingresscontroller
  - nginx
  - (JFV) propositions de maj
---

# FAQ Ingress Controller

## How can I expose my new service with `nginx ingress controller` ?

A Kubernetes Ingress Controller acts as a reverse proxy. We describe here how to use the `nginx ingress controller`.

In the `Ingress`, define a path to the abcdesktop's nginx service.

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-demo
  namespace: abcdesktop
spec:
  rules:
    - host: demo.digital.pepins.net
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx
                port:
                  number: 80
  ingressClassName: nginx
```

The request `path: /` is proxyfied to service named nginx in abcdesktop namespace.


## How to prevent the connection from closing after 60 seconds of inactivity ?

My desktop is disconnected after 60 seconds of inactivity, and the message *"Your abcdesktop session has been disconnected. Please reload this page"* appears.

![abcdesktop session has been disconnected](img/abcdesktopsessionhasbeendisconnected.png)

The message `Your abcdesktop session has been disconnected. Please reload this page` appears when the `websockify` websocket is disconnected.


Add an heartbeat value to send a ping to the client every INTERVAL seconds

Edit the `od.config` file, add to the `desktop.envlocal` option `'WEBSOCKIFY_HEARTBEAT':'30'`

```
desktop.envlocal: { 'WEBSOCKIFY_HEARTBEAT':'30', 'LIBOVERLAY_SCROLLBAR':'0', 'UBUNTU_MENUPROXY':'0', 'X11LISTEN':'tcp' }
```

In this case, the command `/usr/bin/websockify` sends a ping to the client every 30 seconds. This command runs in the user's pod.

Update the configmap abcdesktop-config

```
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config -o yaml --dry-run=client | kubectl replace -n abcdesktop -f -
```

Restart the pyos pod

```
kubectl delete pods -l run=pyos-od -n abcdesktop
```

To get more informations how to
[Keepalive in websockets](https://websockets.readthedocs.io/en/stable/topics/timeouts.html)

Timeout is a main feature to preserve from unnecessary network bandwidth.

## How to prevent the connection from closing after 60 seconds of inactivity with an nginx ingress controller ?

My desktop is disconnected after 60 seconds of inactivity, and the message *Your abcdesktop session has been disconnected. Please reload this page* appears.

To prevent the connection from closing after 60 seconds of inactivity through Ingress Controller, make sure the Ingress Controller isn't configured to automatically terminate long connections.
The default value nginx's ingress controller is 60 seconds.

Update the default values for `nginx.ingress.kubernetes.io/proxy-read-timeout` and `nginx.ingress.kubernetes.io/proxy-send-timeout` annotations to more than 60 seconds.

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-demo
  namespace: abcdesktop
  annotations:
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
spec:
  rules:
    - host: demo.digital.pepins.net
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx
                port:
                  number: 80
  ingressClassName: nginx
```


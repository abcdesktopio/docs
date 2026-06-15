---
tags:
  - cloud
  - gcp
  - ingress
  - timeout
---


# Publish your website as a public secured service

## Requirements


- read the previous chapter [Deploy abcdesktop on GCP with Kubernetes](gcp.md) 
- a GCP account
- your own domain hosted on GCP
- `gcloud` command line interface [gcloud cli](https://docs.cloud.google.com/sdk/docs/install-sdk/)
- `kubectl` command line

### For More Information

- read the google cloud chapter [install-gke-ingress-controller](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/ingress-xlb)

## Overview

In this chapter, we will use a `gke-ingress-controller` to host your abcdesktop service with a public IP address, then configure the DNS zone file to use your own domain name, and enable TLS to secure your service.

## Set up the GKE Ingress controller

In this example, we will use the GKE built-in ingress controller. Before starting, check whether the `HttpLoadBalancing` add-on is enabled on your cluster.
Go to your cluster page on the GCP console, then `Networking`, you should see `HttpLoadBalancing` as enabled, if not enable it and save your changes.

![httploadbalancing enabled](img/httploadbalancing-enabled.png)

Create an ingress resource for GKE using the abcdesktop service and save it as `abcdesktop_host.yaml`.
Update this manifest with your own FQDN, replacing `hello.ingress.gcp.pepins.net` with your own value.

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-abcdesktop
  annotations:
    spec.ingressClassName: "gce"
spec:
  rules:
    - host: hello.ingress.gcp.pepins.net
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: http-router
                port:
                  number: 80
```


We are using the `spec.ingressClassName` class to deploy an external application load balancer.

Apply the Ingress yaml file

```
NAMESPACE=abcdesktop
kubectl apply -f abcdesktop_host.yaml -n $NAMESPACE
```

You should read

```
ingress.networking.k8s.io/ingress-abcdesktop created
```


Verify the ingress resources:

```
NAMESPACE=abcdesktop
kubectl get ingress -n $NAMESPACE
```

The output looks similar to the following:

Wait a few seconds while the `ADDRESS` field is empty
```
NAME                 CLASS    HOSTS                          ADDRESS   PORTS   AGE
ingress-abcdesktop   <none>   hello.ingress.gcp.pepins.net             80      4s
```

When you obtain an `IP ADDRESS`

```
NAME                 CLASS    HOSTS                          ADDRESS         PORTS   AGE
ingress-abcdesktop   <none>   hello.ingress.gcp.pepins.net   35.190.86.108   80      3m14s
```

In the example above, the ingress resource instructs GCE to route each HTTP request using the `/` prefix for the `hello.ingress.gcp.pepins.net` host to the `http-router` backend service running on port 80. In other words, every request to `http://hello.ingress.gcp.pepins.net/` is served by the `http-router` backend service on port 80.

## Update your DNS zone file 

We will associate your `FQDN` (Fully Qualified Domain Name) with the load balancer's IP address.

![cloud dne](img/cloud-dns.png)

This screenshot describes the GCP network console. It shows the `Domain` information. You can also manage your zone file from your own registrar.

### Create new record

In this example, we are going to create a new record `hello.ingress` (`hello.ingress.gcp.pepins.net`) pointing to the `A` address `35.190.86.108`. This IP address is the load balancer IP address.

Press `Add Standard` button, to update your zone file with the new record

![gcp console add record](img/add-fqdn-ingress.png)

Then you should see your record on your domain page 

![record created](img/fqdn-recorded-ingress.png)

From your local device, you can open a web browser

![reach your website from your new name](img/connect-ingress-http.png)

> Web browser doesn't allow usage of websocket without a secure protocol. To log in, you need to use `https` protocol.

As you can see, your website is `Not Secured`. We are going to add an X.509 SSL certificate to secure your service.

## Enable HTTPS

### Configure Google-managed SSL certificates

To enable HTTPS on our exposed service, we will use Google-managed SSL certificates, which are natively integrated in GCP and work seamlessly with a GKE ingress controller.

First you will create a `ManagedCertificate` object, copy the following lines in a `abcdesktop_managed_certificate.yaml` file.

```
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: abcdesktop-cert
spec:
  domains:
    - hello.ingress.gcp.pepins.net
```

Then apply it to the cluster.

```
NAMESPACE=abcdesktop
kubectl apply -f abcdesktop_managed_certificate.yaml -n $NAMESPACE
```

Now, you will need to modify the previously created ingress file and specify the managed certificate the ingress will use in the `annotations` section.


```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-abcdesktop
  annotations:
    spec.ingressClassName: "gce"
    networking.gke.io/managed-certificates: "abcdesktop-cert"
spec:
  rules:
    - host: hello.ingress.gcp.pepins.net
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: http-router
                port:
                  number: 80                         
```

Then apply it to the cluster to start the certificate generation.

```
NAMESCAPE=abcdesktop
kubectl apply -f abcdesktop_host.yaml -n $NAMESPACE
```

You can check that the provisioning started by running the following command

```
NAMESCAPE=abcdesktop
kubectl get managedcertificate -n $NAMESPACE
```

```
NAME                AGE   STATUS
abcdesktop-cert     30s   Provisioning
```

After a few minutes, between 10 and 15, you will see that the status will change from `Provisioning` to `Active`.

```
NAMESCAPE=abcdesktop
kubectl get managedcertificate  -n $NAMESPACE
```

```
NAME                AGE   STATUS
abcdesktop-cert     12m   Active
```

## Reach your website using `https` protocol 

You can now connect to your public abcdesktop website using `https` protocol.

![reach your website using https](img/connect-ingress-https.png)

The status is secured and we get some information from the certificate

![reach your website using https](img/certificate-ok.png)


## Increase ingress connection timeout

By default, a GCE type ingress has a connection timeout of 30 seconds. For abcdesktop, we do not want the connection to the desktop to be dropped every 30 seconds, so we will need to increase the timeout.

Unlike an NGINX type ingress, you cannot add annotations to the ingress YAML file to increase the timeout value. Instead, you must create a `BackendConfig` object and link it to your routing service.

First copy the following lines in a `backend_config_timeout.yaml`

```
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: long-timeout-backend
spec:
  timeoutSec: 1800
```

Apply it to the cluster

```
NAMESPACE=abcdesktop
kubectl apply -f backend_config_timeout.yaml -n $NAMESPACE
```

Then you need to update the `http-router` service to use this `long-timeout-backend` config, copy the following lines in a `http-router.yaml` file.

```
kind: Service
apiVersion: v1
metadata:
  name: http-router
  labels:
    abcdesktop/role: router-od
  annotations:
    cloud.google.com/backend-config: '{"ports":{"80":"long-timeout-backend"}}'
spec:
  selector:
    run: router-od
  ports:
  - protocol: TCP
    port: 443
    targetPort: 443
    name: https
  - protocol: TCP
    port: 80
    targetPort: 80
    name: http
```

- Apply it to the cluster

```
NAMESPACE=abcdesktop
kubectl apply -f http_router.yaml -n $NAMESPACE
```

Now wait a few minutes for GCE to apply the new configuration. After reconnecting to your desktop, the connection should no longer drop after 30 seconds.


> **Note:** By using this method with the GKE ingress controller, the reverse proxy forwards the client's source IP to your cluster, so no additional configuration is required for that purpose.

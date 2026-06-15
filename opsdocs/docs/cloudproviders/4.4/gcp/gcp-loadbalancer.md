---
tags:
  - cloud
  - gcp
  - load balancer
  - AD
---



# Publish your website as a public secured service


## Requirements


- read the previous chapter [Deploy abcdesktop on GCP with Kubernetes](gcp.md) 
- a GCP account
- your own internet domain
- `gcloud` command line interface [gcloud cli](https://docs.cloud.google.com/sdk/docs/install-sdk/)
- `kubectl` command line
- `wget` command line


## Overview

In this chapter, we will use a `loadBalancer` to host your abcdesktop service with a public IP address, then configure the DNS zone file to use your domain name, and enable TLS to secure your service.
 

## Create a new `http-router` service yaml file


The default install configures the `http-router` service as a `nodePort` type. We are going to update the `http-router` service to use a `LoadBalancer` type.

Create a file named `http-router.yaml`

```
kind: Service
apiVersion: v1
metadata:
  name: http-router
  labels:
    abcdesktop/role: router-od
spec: 
  type: LoadBalancer
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

Save your `http-router.yaml` file

Delete the previous service `http-router`

```
NAMESPACE=abcdesktop
kubectl delete service http-router -n $NAMESPACE
service "http-router" deleted
```

Create your new `service/http-router`

```
NAMESPACE=abcdesktop
kubectl apply -f http-router.yaml -n $NAMESPACE
```

You should read on stdout

```
service/http-router created
```

Wait for few minutes, the `EXTERNAL-IP` of service `http-router` stays in `Pending` state

```
NAMESPACE=abcdesktop
kubectl get services http-router -n $NAMESPACE 
```

```
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
http-router   LoadBalancer   34.118.231.121   <pending>     443:31089/TCP,80:32012/TCP   4s
```

Check the EXTERNAL-IP of service `http-router` again

```
NAMESPACE=abcdesktop
kubectl get services http-router -n $NAMESPACE       
```

> Great the service gets `34.59.246.150` as an `EXTERNAL-IP`

```      
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
http-router   LoadBalancer   34.118.231.121   34.59.246.150   443:31089/TCP,80:32012/TCP   33s
```

You can open a web browser to reach your abcdesktop service with the IP address


![web browser to reach your abcdesktop service](img/external-ip.png)


Web browser doesn't allow usage of websocket without a secure protocol. To log in, you need to use `https` protocol.


## Update your DNS zone file 


We will use a `FQDN` (Fully Qualified Domain Name) to replace the IP address.


![gcp networking](img/cloud-dns.png)

This screenshot describes the GCP network console. It shows the `Domain` information. You can also manage your zone file from your own registrar.
For more information about Cloud DNS, see the [documentation](https://docs.cloud.google.com/dns/docs/tutorials/create-domain-tutorial).

### Create new record

We are going to create a new record `hello.loadbalancer` (`hello.loadbalancer.gcp.pepins.net`) pointing to the `A` address `34.59.246.150`. Setting a low `TTL` value is recommended to allow faster propagation of changes.

The IP Address is show by the GCP network console, it is the same address as the `EXTERNAL-IP` of your `http-router` service.

```
NAMESPACE=abcdesktop
kubectl get services http-router -n $NAMESPACE
```

returns a `EXTERNAL-IP`

```
NAME          TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
http-router   LoadBalancer   34.118.231.121   34.59.246.150   443:31089/TCP,80:32012/TCP   33s
```

Press `Add Standard` button, to update your zone file with the new record

![gcp console add record](img/add-fqdn.png)

Then you should see your record on your domain page 

![record created](img/record-created.png)

From your local device, you can open a web browser

![reach your website from your new name](img/http-fqdn.png)


Web browser doesn't allow usage of websocket without a secure protocol. To log in, you need to use `https` protocol.

As you can see, your website is `Not Secured`. We are going to add an X.509 SSL certificate to secure your service.



## Obtain a Certificate

If you already have an X.509 certificate with private and public key files for your website, you can skip this section.

To create an SSL certificate, this guide uses the Let's Encrypt service. You will need your hostname and your email address.

Define the new variables `ABCDESKTOP_PUBLIC_FQDN` and `USER_EMAIL_ADDRESS` 


``` bash
NAMESPACE=abcdesktop
ABCDESKTOP_PUBLIC_FQDN=hello.loadbalancer.gcp.pepins.net
USER_EMAIL_ADDRESS=thisisyouremail@domain.com
ROUTER_POD_NAME=$(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name}  -n abcdesktop)
kubectl exec -n $NAMESPACE -it ${ROUTER_POD_NAME} -- /usr/bin/certbot certonly --webroot -w /var/lib/nginx/html -d ${ABCDESKTOP_PUBLIC_FQDN} -m "${USER_EMAIL_ADDRESS}" --agree-tos -n
```

You should read on stdout

```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Account registered.
Requesting a certificate for hello.loadbalancer.gcp.pepins.net

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/hello.loadbalancer.gcp.pepins.net/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/hello.loadbalancer.gcp.pepins.net/privkey.pem
This certificate expires on 2026-04-08.
These files will be updated when the certificate renews.

NEXT STEPS:
- The certificate will need to be renewed before it expires. Certbot can automatically renew the certificate in the background, but you may need to take steps to enable that functionality. See https://certbot.org/renewal-setup for instructions.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

```

The files `fullchain.pem` and `privkey.pem` are located inside the container. 

```
Certificate is saved at: /etc/letsencrypt/live/hello.loadbalancer.gcp.pepins.net/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/hello.loadbalancer.gcp.pepins.net/privkey.pem
```

We export the files and create a new secrets. 


```
NAMESPACE=abcdesktop
kubectl exec -n $NAMESPACE -it  ${ROUTER_POD_NAME} -- cat /etc/letsencrypt/live/$ABCDESKTOP_PUBLIC_FQDN/fullchain.pem > fullchain.pem
kubectl exec -n $NAMESPACE -it  ${ROUTER_POD_NAME} -- cat /etc/letsencrypt/live/$ABCDESKTOP_PUBLIC_FQDN/privkey.pem > privkey.pem
```


## Create a Secret for the X.509 Certificate


Create a secret named `http-router-certificat` with the `fullchain.pem` and `privkey.pem` file content

```
NAMESPACE=abcdesktop
kubectl create secret tls http-router-certificat --cert=fullchain.pem --key=privkey.pem -n $NAMESPACE 
```

Your secret is created

```
secret/http-router-certificat created
```


## Update `http-router` ConfigMap to use the new `http-router-certificat` secret

Download [abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml) file 

```
wget https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml
```

Open your `abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml` file, look for the ConfigMap `abcdesktop-routehttp-config`.

Remove the comments to enable https and change the value `YOUR_SERVER_NAME_AND_DOMAIN` by your own value. 

```
 # nginx server config
 server {
     ...
     
     ######
     # uncomment this to enable https
     #
     listen 443 ssl http2 default_server;
     listen [::]:443 ssl http2 default_server;
     server_name YOUR_SERVER_NAME_AND_DOMAIN; # change this too
     ssl_certificate     /etc/nginx/ssl/tls.crt;
     ssl_certificate_key /etc/nginx/ssl/tls.key;
     #
     # end of https section
     ######
     
     ...
     index index.html index.htm;
```

For example

```
     listen 443 ssl http2 default_server;
     listen [::]:443 ssl http2 default_server;
     server_name hello.loadbalancer.gcp.pepins.net;
     ssl_certificate     /etc/nginx/ssl/tls.crt;
     ssl_certificate_key /etc/nginx/ssl/tls.key;
```

Apply your new nginx configuration file

```
NAMESPACE=abcdesktop
kubectl apply -f abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml -n $NAMESPACE
```
 
## Update `deployment` http-router
 
Update the `deployment` route to add the SSL certificate entry

The `abcdesktop-deployment-routehttps.{{ abcdesktop.latest_release }}.yaml` file  adds `mountPath: /etc/nginx/ssl` to `secretName: http-router-certificat`

```
NAMESPACE=abcdesktop
kubectl apply -f https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-deployment-routehttps.{{ abcdesktop.latest_release }}.yaml -n $NAMESPACE
```

You should read on stdout 

```
deployment.apps/router-od configured
```


## Reach your website using `https` protocol 

You can now connect to your public abcdesktop website using `https` protocol.

![reach your website using https](img/https-fqdn.png)


The status is secured and we get some information from the certificate

![reach your website using https](img/cert-viewer.png)

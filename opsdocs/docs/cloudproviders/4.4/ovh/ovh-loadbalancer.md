# Publish your website as a public secured service


## Requirements


- Read the previous chapter [Deploy abcdesktop on OVHcloud with Kubernetes](ovh.md) 
- an OVHcloud account
- your own internet domain
- `kubectl` command line
- `wget` command line


## Overview

In this chapter, you will use a `LoadBalancer` service to expose your abcdesktop instance with a public IP address, configure your DNS zone file to use your domain name, and enable TLS to secure the service.
 

## Create a new `http-router` service yaml file


The default installation configures the `http-router` service as a `nodePort` type. We will update the `http-router` service to use a `LoadBalancer` type.

Create a file named `http-router.yaml`:

```
kind: Service
apiVersion: v1
metadata:
  name: http-router
  labels:
    abcdesktop/role: router-od
  annotations:
    service.beta.kubernetes.io/ovh-loadbalancer-healthcheck-protocol: "HTTP"
    service.beta.kubernetes.io/ovh-loadbalancer-healthcheck-port: "80"
    service.beta.kubernetes.io/ovh-loadbalancer-healthcheck-path: "/healthz"
    service.beta.kubernetes.io/ovh-loadbalancer-protocol: "HTTP"
    service.beta.kubernetes.io/ovh-loadbalancer-tls-ports: "443"
    service.beta.kubernetes.io/ovh-loadbalancer-tls-passthrough: "true"
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

Save the `http-router.yaml` file.

Delete the previous `http-router` service:

```
kubectl delete service http-router -n abcdesktop
service "http-router" deleted
```

Create the new `service/http-router`:

```
kubectl apply -f http-router.yaml -n abcdesktop
service/http-router created
```

Wait a few minutes; the `EXTERNAL-IP` of the `http-router` service remains in `Pending` state:

```
kubectl get services http-router -n abcdesktop 
```

```
NAME          TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)                      AGE
http-router   LoadBalancer   10.3.114.1   <pending>     443:31379/TCP,80:31570/TCP   12s
```

Check the `EXTERNAL-IP` of the `http-router` service again:

```
kubectl get services http-router -n abcdesktop       
```

> The service has been assigned `51.83.253.201` as its `EXTERNAL-IP`.

```      
NAME          TYPE           CLUSTER-IP   EXTERNAL-IP     PORT(S)                      AGE
http-router   LoadBalancer   10.3.114.1   51.83.253.201   443:31379/TCP,80:31570/TCP   5m17s

```

Open a web browser to access your abcdesktop service using the IP address.


![web browser to reach your abcdesktop service](img/ip-connect.png)


Web browsers block WebSocket connections without a secure protocol. To log in, use the `https` protocol.


## Update your DNS zone file 


We will use a `FQDN` (Fully Qualified Domain Name) to replace the IP address.


![ovh networking](img/ovh-networking.png)

This screenshot shows the OVHcloud network console, displaying the **Domain** configuration. You can also manage your zone file directly through your domain registrar.

### Create new record

Create a new `A` record named `hello` (e.g., `hello.ovhcloud.pepins.net`) pointing to `51.83.253.201`.

The IP address is shown in the OVHcloud network console and corresponds to the `EXTERNAL-IP` of your `http-router` service.

```
kubectl get services http-router -n abcdesktop
NAME          TYPE           CLUSTER-IP   EXTERNAL-IP     PORT(S)                      AGE
http-router   LoadBalancer   10.3.114.1   51.83.253.201   443:31379/TCP,80:31570/TCP   5m17s
```

![ovh console domain overview](img/createrecord.png)

Click `Create Record` to update your zone file with the new record.

![ovh console domain record added](img/recorddone.png)

From your local device, open a web browser.

![reach your website from your new name](img/hello_http.png)


Web browsers block WebSocket connections without a secure protocol. To log in, use the `https` protocol.

Your website is marked as `Not Secured`. You must add an X.509 SSL certificate to secure the service.



## Obtain a Certificate

If you already have an X.509 certificate with private and public key files for your website, you can skip this section.

To obtain an SSL certificate, this guide uses the Let's Encrypt service. You will need your new hostname and your email address.

Define the variables `ABCDESKTOP_PUBLIC_FQDN` and `USER_EMAIL_ADDRESS`:


``` bash
ABCDESKTOP_PUBLIC_FQDN=hello.ovhcloud.pepins.net
USER_EMAIL_ADDRESS=thisisyouremail@domain.com
ROUTER_POD_NAME=$(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name}  -n abcdesktop)
kubectl exec -n abcdesktop -it ${ROUTER_POD_NAME} -- /usr/bin/certbot certonly --webroot -w /var/lib/nginx/html -d ${ABCDESKTOP_PUBLIC_FQDN} -m "${USER_EMAIL_ADDRESS}" --agree-tos -n
```

You should see the following output:

```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Account registered.
Requesting a certificate for hello.ovhcloud.pepins.net

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/hello.ovhcloud.pepins.net/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/hello.ovhcloud.pepins.net/privkey.pem
This certificate expires on 2026-04-21.
These files will be updated when the certificate renews.

NEXT STEPS:
- The certificate will need to be renewed before it expires. Certbot can automatically renew the certificate in the background, but you may need to take steps to enable that functionality. See https://certbot.org/renewal-setup for instructions.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

The `fullchain.pem` and `privkey.pem` files are stored inside the container.

```
Certificate is saved at: /etc/letsencrypt/live/hello.ovhcloud.pepins.net/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/hello.ovhcloud.pepins.net/privkey.pem
```

Export the certificate files and create a new Kubernetes secret.


```
kubectl exec -n abcdesktop -it  ${ROUTER_POD_NAME} -- cat /etc/letsencrypt/live/$ABCDESKTOP_PUBLIC_FQDN/fullchain.pem > fullchain.pem
kubectl exec -n abcdesktop -it  ${ROUTER_POD_NAME} -- cat /etc/letsencrypt/live/$ABCDESKTOP_PUBLIC_FQDN/privkey.pem > privkey.pem
```


## Create a Secret for the X.509 Certificate

Create a Kubernetes secret named `http-router-certificat` using the `fullchain.pem` and `privkey.pem` file contents.

```
kubectl create secret tls http-router-certificat --cert=fullchain.pem --key=privkey.pem -n abcdesktop 
```

The secret has been created.

```
secret/http-router-certificat created
```


## Update `http-router` ConfigMap to use the new `http-router-certificat` secret

Download [abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml)

```
wget https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml
```

Open the `abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml` file and locate the ConfigMap named `abcdesktop-routehttp-config`.

Uncomment the HTTPS section and replace `YOUR_SERVER_NAME_AND_DOMAIN` with your actual server name and domain.

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

For example:

```
     listen 443 ssl http2 default_server;
     listen [::]:443 ssl http2 default_server;
     server_name hello.ovhcloud.pepins.net;
     ssl_certificate     /etc/nginx/ssl/tls.crt;
     ssl_certificate_key /etc/nginx/ssl/tls.key;
```

Apply the updated NGINX configuration file:

```
kubectl apply -f abcdesktop-routehttp-config.{{ abcdesktop.latest_release }}.yaml -n abcdesktop
```
 
## Update `deployment` http-router
 
Update the `deployment` route to add the SSL certificate entry.

The `abcdesktop-deployment-routehttps.{{ abcdesktop.latest_release }}.yaml` file adds `mountPath: /etc/nginx/ssl` to `secretName: http-router-certificat`.

```
kubectl apply -f https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-deployment-routehttps.{{ abcdesktop.latest_release }}.yaml -n abcdesktop
```

## Reach your website using `https` protocol 

You can now connect to your abcdesktop public website using the `https` protocol.

![reach your website using https](img/hello_https.png)


The connection is secured. You can inspect the certificate details.


![reach your website using https](img/certificate-ok.png)

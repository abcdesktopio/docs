---
title: Configure a Reverse Proxy in Front of abcdesktop.io | abcdesktop.io
description: Guide to placing a reverse proxy such as nginx or Apache in front of abcdesktop.io, including WebSocket proxy configuration and default_host_url update.
keywords: reverse proxy, nginx, Apache, WebSocket, proxy, abcdesktop, Kubernetes, configuration, HTTPS
tags:
  - FAQ
  - reverse proxy
  - nginx
  - configuration
---

# How to Add a Reverse Proxy in Front of abcdesktop

This chapter describes how to add a reverse proxy in front of abcdesktop. It covers the `nginx` configuration required to place a reverse proxy in front of an abcdesktop deployment.

First, update the `od.config` file to set the `default_host_url` to your external URL.

## Edit Your Configuration File

In this example, the external URL is `https://abcdesktop.domain.com`.

```
# DEFAULT HOST URL 
# public host url of the service
# change this with your URL or
# set the external URL service if you use a reverse proxy
default_host_url : 'https://abcdesktop.domain.com'
# END OF DEFAULT HOST URL
```

If the `od.config` file does not exist, extract it from the `abcdesktop-config` ConfigMap to a local file:

```bash
kubectl -n abcdesktop get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
```

This command outputs the current configuration to a local file named `od.config`.

Edit the `od.config` file using your preferred editor:

```bash
vim od.config
```

- Update the `default_host_url` value:

```
default_host_url : 'https://abcdesktop.domain.com'
```

- Apply the changes.

To apply the changes, replace the `abcdesktop-config` ConfigMap by running the `kubectl replace` command, then restart the `pyos` deployment using `rollout restart`.

```bash
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config  -o yaml --dry-run | kubectl replace -n abcdesktop -f -
kubectl rollout restart deployment pyos-od -n abcdesktop
```

Once the configuration is updated, create the reverse proxy configuration for your preferred proxy server — either `nginx` or `haproxy`.


## Create Your Reverse Proxy

### Add `nginx` as a Reverse Proxy in Front of abcdesktop

- Create a WebSocket configuration file named `ws.conf`:

```
proxy_buffering 	off;
proxy_http_version 	1.1;

# Add proxy header
proxy_set_header X-Forwarded-For 	$proxy_add_x_forwarded_for;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_set_header Accept-Language 	$http_accept_language;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header Authorization $http_authorization;

# pass to $my_node
proxy_pass $my_node;
```


- Create a proxy configuration file named `proxy.conf`:

```
# Add proxy header
proxy_set_header User-Agent $http_user_agent;
proxy_set_header Accept-Language $http_accept_language;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Origin $http_origin;
proxy_set_header Host $host;

# pass to $my_node
proxy_pass 	 $my_node;
```



- Create the reverse proxy configuration file named `reverse-abcdesktop.conf`:


```
server {
listen 443;
server_name abcdesktop.domain.com;
index index.html index.htm;

####
# make changes
#
resolver a.b.c.d; # change here your own ip address of your dns resolver
set $my_node http://$YOUR_INTERNAL_SERVICE:$PORT; # change here your own internal service and port

### enable ssl 
# ssl on;
# ssl_certificate /etc/letsencrypt/live/abcdesktop.domain.com/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/abcdesktop.domain.com/privkey.pem;
#
# end of recommended changes
#### 

add_header X-Frame-Options "SAMEORIGIN";

# broadcast websocket 
# if more than one device is connected to the same pod
# also use to send internal message 
location /broadcast { 
  include ws.conf;
}

# printer websocket
location /printer {
  include ws.conf;
}

# terminal websocket (bash)
location /terminals/ {
	proxy_send_timeout 600s;
   proxy_read_timeout 600s;
   include ws.conf;
	break;
}

# vnc websocket
location /websockify {
	# need between 1s and 3s to start a new user container
	# 20s should be enough
	proxy_connect_timeout 20;

	# Keep the websocket alive during 10 m 
	proxy_send_timeout 600;
	proxy_read_timeout 600;
	include ws.conf;
}

# speedtest http 
# Upload and Download test file for speedtest up to 128M
location /speedtest {
	client_max_body_size 128M;
	proxy_buffering on;
	include proxy.conf;
}

# http filter
# upload file to homedir max size is 4G 
location /filer {
	client_max_body_size 4G;
   include proxy.conf;
}

# default route
location / {
    # 180s max size to create desktop pod
	proxy_read_timeout 180s;
	proxy_send_timeout 180s;
   include proxy.conf;
}
```

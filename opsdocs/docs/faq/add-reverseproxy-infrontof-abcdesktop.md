# How to add a reverse proxy in front of abcdesktop

This chapter describe host to add a reverse proxy in front of abcdesktop. 
- One chapter describes the `nginx` configuration in front of abcdesktop
- One chapter describes the `haproxy` configuration in front of abcdesktop

For both of them, you need to update `od.config` file to set the `default_host_url` as your `external url` 

## Edit your configuration file


In this example, the `external url` is `https://abcdesktop.domain.com`

```
# DEFAULT HOST URL 
# public host url of the service
# change this with your URL or
# set the external URL service if you use a reverse proxy
default_host_url : 'https://abcdesktop.domain.com'
# END OF DEFAULT HOST URL
```

If the `od.config` file does not exist, extract it from the abcdesktop-config configmap to a local file `od.config`

```bash
kubectl -n abcdesktop get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
```

You get a the new local file `od.config`

To make change, edit your own `od.config` file with your favorite file editor:

```bash
vim od.config
```

- Update the value `default_host_url 

```
default_host_url : 'https://abcdesktop.domain.com'
```

- Apply changes

To apply changes, you have to replace the `abcdesktop-config`, by running the `replace kubectl` command line option. Then `rollout restart`the `pyos` pod.

```bash
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config  -o yaml --dry-run | kubectl replace -n abcdesktop -f -
kubectl rollout restart deployment pyos-od -n abcdesktop
```


Great, now we can create the configuration for the reverse proxy of your choice, `nginx` or `haproxy`.


## Create your reverse proxy 



### Add `nginx` as a reverse proxy in front of abcdesktop

- Create a websocket config file named `ws.conf`

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


- create a proxy config file named `proxy.conf`

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



- create the reverse proxy config file named `reverse-abcdesktop.conf`


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



### Add `haproxy` as a reverse proxy in front of abcdesktop
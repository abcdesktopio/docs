# Nginx oc.nginx 

Nginx is used as a reverse proxy server for HTTP, HTTPS protocols, as well as a load balancer, HTTP cache, and a web server (origin server). 

## Nginx routing

```
                                     +--------------------+
                                +--->|       oc.user      |
                                |    +----------+---------+
                                |               
              +-----------+     |               
              |           |     |    +----------+---------+           +---------------+
Webuser +---->|   nginx   |-----+--->| od.py (port 8000)  |---------->|    mongodb    |
              |           |     |    +--------------------+           +---------------+
              +-----------+     |
                                |
                                |    +--------------------+
                                +--->|   static web site  |
                                     +--------------------+

```


## Nginx Configuration

* Read the nginx [nginx.conf](https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/nginx.conf) configuration file
* Read the nginx [default web site](https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/sites-enabled/default) configuration file
* Read the [route.conf](https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/route.conf) configuration file, use to route HTTP request 
* Read the [proxy.conf](https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/proxy.conf) configuration file, use to proxy HTTP request 



### Web site

The web site source code is stored in the /var/webModules directory.

### main reverse proxy 

- moauth|fauth|gauth|oauth|autologin|API|status are routed to od.py ```http://$my_proxy:$api_service_tcp_port;```
- /spawner is routed to nodejs spawner service ```http://$target:$spawner_service_tcp_port;```
- /websockify is routed to websocket ```http://$target:$ws_tcp_bridge_tcp_port/;```
- /u8_1_11025 is routed to pulseaudio sound service ```http://$target:$pulseaudio_http_port/listen/source/u8_1_11025.monitor;```
- /filer is routed to nodejs filer service http://$target:8080 
- /broadcast is routed to nodejs broadcast service ```http://$target:$broadcast_tcp_port;```


## LUA scripts

The /etc/nginx/get.targetmap.lua read the ```jwt_token``` and return the ip address or the pod's fqdn, using the ```jwt_desktop_signing_public_key``` and the ```jwt_desktop_payload_private_key```

It uses a targetmap (dict) as first cache level.


```
lua_shared_dict targetmap 1m;
```

Read the lua script [get.targetmap.lua](https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/get.targetmap.lua) to get details jwt token data and payload encryption.


# Nginx route

Nginx is used as a reverse proxy server for HTTP, HTTPS protocols, as well as a load balancer, HTTP cache, and a web server (origin server). 

## Nginx routing

Route image is an `openresty` http server, based on `nginx`

## Nginx Configuration

* The nginx [nginx.conf]([https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/nginx.conf](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/nginx.conf)) configuration file
* The routing table [route.conf]([https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/route.conf](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/route.conf)) configuration file
* The configuration file for HTTP headers  [proxy.conf](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/proxy.conf)

### main reverse proxy routes

- `'/'` route to `http://website` 
- `/API` route to `http://pyos`
- `/terminals` route to user pod `http://$target:$xterm_tcp_port` where `$target` is the ip address of the pod
- `/spawner` route to user pod `http://$target:$spawner_service_tcp_port` where `$target` is the ip address of the pod
- `/websockify` oute to user pod `http://$target:$ws_tcp_bridge_tcp_port` where `$target` is the ip address of the pod
- `/filer` route to http user pod service `http://$target:$file_service_tcp_port` where `$target` is the ip address of the pod
- `/printerfiler` route to http `http://$target:$printerfile_service_tcp_port` where `$target` is the ip address of the pod
- `/broadcast` route to http user pod  `http://$target:$broadcast_tcp_port` where `$target` is the ip address of the pod
- `/sound` route to websocket user pod `http://$target:$sound_service_tcp_port` where `$target` is the ip address of the pod


### default desktop oc.user tcp port 

```
  set $pulseaudio_http_port               4714;
  set $ws_tcp_bridge_tcp_port             6081;
  set $xterm_tcp_port                     29781;
  set $printerfile_service_tcp_port       29782;
  set $file_service_tcp_port              29783;
  set $broadcast_tcp_port                 29784;
  set $snaphost_service_tcp_port          29785;
  set $spawner_service_tcp_port           29786;
  set $signalling_service_tcp_port        29787; 
  set $sound_service_tcp_port             29788;
  set $microphone_service_tcp_port        29789;
```

## LUA scripts

The /etc/nginx/get.targetmap.lua read the ```jwt_token``` and return the ip address or the pod's fqdn, using the ```jwt_desktop_signing_public_key``` and the ```jwt_desktop_payload_private_key```

It uses a targetmap (dict) as first cache level.

```
lua_shared_dict targetmap 1m;
```
Read the lua script [get.targetmap.lua](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/get.targetmap.lua) to get details jwt token data and payload encryption.


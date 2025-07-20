# route

`route` is used as a reverse proxy server for HTTP, HTTPS protocols, as well as a load balancer, HTTP cache. 

## HTTP routing

The `route` image is an `openresty` http server, based on `nginx` with embeded `lua` engine.

## route configuration

* The nginx [nginx.conf]([https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/nginx.conf](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/nginx.conf)) configuration file
* The routing table [route.conf]([https://github.com/abcdesktopio/oc.nginx/blob/main/etc/nginx/route.conf](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/route.conf)) configuration file
* The configuration file for HTTP headers  [proxy.conf](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/proxy.conf)

### reverse proxy routes

- `'/'` route to `http://website` 
- `/API` route to `http://pyos`
- `/terminals` route to user pod `http://$target:$xterm_tcp_port` where `$target` is the ip address of the pod
- `/spawner` route to user pod `http://$target:$spawner_service_tcp_port` where `$target` is the ip address of the pod
- `/websockify` oute to user pod `http://$target:$ws_tcp_bridge_tcp_port` where `$target` is the ip address of the pod
- `/filer` route to http user pod service `http://$target:$file_service_tcp_port` where `$target` is the ip address of the pod
- `/printerfiler` route to http `http://$target:$printerfile_service_tcp_port` where `$target` is the ip address of the pod
- `/broadcast` route to http user pod  `http://$target:$broadcast_tcp_port` where `$target` is the ip address of the pod
- `/sound` route to websocket user pod `http://$target:$sound_service_tcp_port` where `$target` is the ip address of the pod


### default desktop tcp port 

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

The script `/etc/nginx/get.targetmap.lua` reads the `jwt_token` and returns the ip address or fqdn of the user's pod.
To verify the JWT delivery that had been signed by `pyos`, it utilizes the `jwt_desktop_signing_public_key` (rsa public key).
Then it decrypts the jwt payload with the `jwt_desktop_payload_private_key` (another rsa private key) to get the ip address of the user pod, and routes the http request to the pod.

`targetmap` (dict) is a first cache level. When a `jwt_token` is decoded the target ip address is added to the `targetmap` cache to reduce cpu usage of the reverse proxy.
Each entries in `targetmap` cache has a time to live of 600 secondes by default.


```
lua_shared_dict targetmap 1m;
```
Read the lua script [get.targetmap.lua](https://github.com/abcdesktopio/route/blob/4.1/etc/nginx/get.targetmap.lua) to get details jwt token data and payload encryption.


# Memcached

The [memcached](https://hub.docker.com/_/memcached/) container comes from the public docker registry. This service is attend to the netback network. 


memcached store pods and containers message during the create process.


## create desktop 

### create desktop message 

Messages stored into memcache 

|status| user message				|
|------|----------------------------|
| OK   |'Looking for your desktop'  |
| OK   |'Looking for your desktop done' |
| OK   |'Building desktop'|
| OK   |'Starting network services, it will take a while...'|
| OK   |'Network services started.'|
| OK   |'Starting desktop graphical service %ds / %d' % (nCount,nCountMax) |
| OK   |'Starting desktop spawner service %ds / %d' % (nCount,nCountMax) |
| OK   |'Desktop services are ready after %d s'|
| Error| 'createDesktop error - myOrchestrator.createDesktop %s'  |


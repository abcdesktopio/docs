# Memcached

The [memcached](https://hub.docker.com/_/memcached/) container comes from the public docker registry. This service is attend to the netback network. 

## Association table beetween session_id and ip address 

[Memcached](https://memcached.org) is used to share datas between nginx and os.py. When os.py creates a new container, it gets the container ip address on the netuser overlay network and set a key value to memcache. The key is the session_id, the value is the container ip address.
When a new request is recieve by nginx, nginx try to find the associated ip adress in his own cache data using the session_id, if the session_id is not found, nginx ask memcached to get the ip address associated.


TODO: change the expiration time

The key value data expired by default in (30 days). The number of seconds may not exceed 2592000 (30 days) in memcache. So the maximum expiration time is 30 days.


TODO: change access permissions to memcached



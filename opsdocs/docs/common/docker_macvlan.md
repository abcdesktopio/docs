# Using docker macvlan network


## How do I attach the abcdesktop user's container directly to my local network? 

This article come from [using-docker-macvlan-networks](https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/)

One possible answer to that question is the macvlan network type, which lets you create “clones” of a physical interface on your host and use that to attach containers directly to your local network. 


On my local network, my DHCP server will not assign any addresses before 192.168.8.100. I have decided to assign to Docker the subset 192.168.8.64/27, which is a range of 32 address starting at 192.168.8.64 and ending at 192.168.8.95. The corresponding docker network create command would be:


``` bash
docker network create -d macvlan --subnet=192.168.8.0/24 --gateway=192.168.8.1 --ip-range=192.168.8.64/27 -o parent=eno1 abcdesktop_netuser
```

Now it is possible to create containers attached to my local network without worrying about the possibility of ip address conflicts.

## Edit the docker-compose.yml file

Change the networks description in the default docker-compose.yml file.

Edit the networks section. The complete docker-compose.yml file is now :

``` yaml
version: '3'
services:
  pyos:
    depends_on:
      - memcached
      - mongodb
    image: 'abcdesktopio:oc.pyos'
    networks:
      - netback
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
  speedtest:
    image: 'abcdesktopio:oc.speedtest'
    networks:
      - netback
  nginx:
    depends_on:
      - memcached
      - pyos
    image: 'abcdesktopio:oc.nginx'
    ports:
      - '80:80'
      - '443:443'
    networks:
      - abcdesktop_netuser
      - netback
  memcached:
    image: memcached
    networks:
      - netback
  mongodb:
    image: mongo
    networks:
      - netback
networks:
  abcdesktop_netuser:
    external: true
  netback:
    internal: true
```


Run the docker-compose with the new ```docker-compose.yml``` file

```
docker-compose -p abcdesktop up
```


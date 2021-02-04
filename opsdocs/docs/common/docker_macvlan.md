# Using docker network for an application


## Requirements 


## Goals
* Use a dedicated network for an application. For example bind the application Firefox to a dedicated docker network. 
This network can be a macvlan, ipvlan or an SRIOV network


## Architecture

When abcdesktop create a docker container, abcdesktop can set a dedicated network for this container.




## Create a dedicated network 

On your worker nodes :
* create a dedicated network interface to brige the new network interface 

You have to choose a nework driver for example macvlan, ipvlan 

Example :

Create a network abcnetfirefox with the driver macvlan and bridge the network interface eno1 with the vlan 123 

``` bash
docker network create -d macvlan --subnet=192.168.8.0/24 --gateway=192.168.8.1 --ip-range=192.168.8.64/27 -o parent=eno1.123 abcnetfirefox
```

Make sure that's you can reach the default gateway and the dns server for container.
In this example, just start a busybox to :
* ping the default gateway
* run nslookup to query www.google.com ip address

``` bash
docker --remove --network abcnetfirefox busybox ping 192.168.8.1
docker --remove --network abcnetfirefox busybox nslookup www.google.com
```

## Applications rules

Update your applist.json file and add a specific rule into the firefox application description 

Specific rules entry

```
"rules": { "homedir": { "default": true, "ship": true }, 
           "network": { "default": false, 
                        "internet": { "name": "abcnetfirefox", "dns": [ "8.8.8.8" ] } } },
```
In this example, if the current user toekn contains the tag label ```internet``` when the firefox application use ```abcnetfirefox``` and the dns ```8.8.8.8```

Build and update your new firefox application

Update you pyos 

## Tag the user auth 

Add a tag 'internet' to the user auth provider




## 





## How do I attach the abcdesktop user's container directly to my local network? 

This article come from [using-docker-macvlan-networks](https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/)

``` bash
docker network create -d macvlan --subnet=192.168.8.0/24 --gateway=192.168.8.1 --ip-range=192.168.8.64/27 -o parent=eno1 abcdesktop_firefox
```


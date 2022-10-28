# Edit pyos core service configuration file 


Update the Pyos core service configuration file depends, if your are running abcdesktop.io on native Docker (Non-Cluster Host) or in Kubernetes mode.

* In Kubenetes Mode: Read the setup guide, to make change in the abcdesktop yaml file. [Setup and configuration guide for kubernetes abcdesktop](../setup/kubernetes_abcdesktop.md)

* In Docker Mode : Read the following chapter


This chapter 'Edit Pyos configuration file', apply **only for native Docker (Non-Cluster Host)**, read the dedicated chapter if you are running abcdesktop.io with a kubernetes cluster.

## Edit Pyos code service configuration file in docker mode

### Requirements

- A running dockerd last version 
- An access to the docker public registry
- The ```docker-compose``` command ready to run


#### Download sample configuration file

Create a directotry named ```abcdesktop``` in your home directory.

```
cd
mkdir -p abcdesktop
```


To edit you configuration file in abcdesktop.io docker mode, download the sample configuration file and save it as ```od.config``` where docker-compose.yml file
is located.


[Download sample configuration file od.config](https://raw.githubusercontent.com/abcdesktopio/pyos/main/od.config.reference) then rename the ```od.config.reference``` file as ```od.config```

### Stop your docker-compose
```
 docker-compose down
```

You should read on the standart output

```
Removing open_nginx_1     ... done
Removing open_pyos_1      ... done
Removing open_memcached_1 ... done
Removing open_speedtest_1 ... done
Removing open_mongodb_1   ... done
Network netuser is external, skipping
Network netback is external, skipping
```


### Edit your ```docker-compose.yml```

Edit your ```docker-compose.yml``` to add a volumes entry to pyos services

> Example :  
> My working directory is ```/home/alex/abcdesktop```

Add the new entry in volumes	

```
 volumes:
      - /home/alex/abcdesktop/od.config:/var/pyos/od.config
```

For example, the ```docker-compose.yml``` contains

```
version: '3'
services:
  pyos:
    depends_on:
      - memcached
      - mongodb
    image: 'abcdesktopio/oc.pyos'
    networks:
      - netback
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/alex/abcdesktop/od.config:/var/pyos/od.config
  speedtest:
    image: 'abcdesktopio/oc.speedtest'
    networks:
      - netuser
  nginx:
    depends_on:
      - memcached
      - pyos
    image: 'abcdesktopio/oc.nginx'
    ports:
      - '80:80'
      - '443:443'
    networks:
      - netuser
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
  netuser:
    driver: bridge
  netback:
    internal: true
```

### Edit your configuration file 

Now, it's time to make a change in your od.config file.

Download the od.config file and save it to your abcdesktop local directory.

To make change, edit your own ```od.config``` file

```
vim od.config 
```

Change the defaultbackgroundcolors in the desktop options.

Locate the line ```desktop.defaultbackgroundcolors``` and update the first entries with the values ``` '#FF0000', '#FFFFFF',  '#0000FF' ```

```
desktop.defaultbackgroundcolors : [ '#FF0000', '#FFFFFF',  '#0000FF', '#CD3C14', '#4BB4E6', '#50BE87', '#A885D8', '#FFB4E6' ]
```

Save your local oc.config file.


Run your docker-compose

To restart your docker-compose, run the command

```
 docker-compose up
```

> When the od.config change, od.py reload this configuration file automatically. 

You should read at the standard ouput of docker-compose

```
Starting abcdesktop_speedtest_1 ... done
Starting abcdesktop_mongodb_1   ... done
Starting abcdesktop_memcached_1 ... done
Starting abcdesktop_openldap_1  ... done
Starting abcdesktop_pyos_1      ... done
Starting abcdesktop_nginx_1     ... done
[ lines cut here ]
```


### Check that the new colors are painted in front :

Open the url http://localhost, in your web browser, to start a simple abcdesktop.io container. 

```
http://localhost
```

You should see the abcdesktop.io home page.

Press the ```Sign-in Anonymously, have look```

At the right top corner, click on the menu and choose ```Settings```, then click on ```Screen Colors```

Choose your colors and you should have it as background color :

![newbackgroundcolors](img/newbackgroundcolors.png)

Great, you can easily update your configuration file od.config. We will make some changes during the next exercices.


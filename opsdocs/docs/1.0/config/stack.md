
# stack entry in od.config


## stack.mode

```stack.mode``` describes how abcdesktop.io can manage user's containers and application. 

* If you run a docker only daemon, set the value to ```standalone```.
* If you run a kubernetes cluster, set the value to ```kubernetes ```.

| stack.mode         | Description |
|--------------------|-------------|
|  ```standalone```  | Use a dockerd only, this is for personal usage  |
|  ```kubernetes```  | Use a kubernetes services | 



## stack.kubernetesdefaultdomain

```stack.kubernetesdefaultdomain``` is the default domain name configured in kubernetes cluster. This value is type is string and only read if stack.mode is ```kubernetes```.

The default value is ```abcdesktop.svc.cluster.local``` 

If option value ```mongodb``` or ```memcached``` are set, the values are NOT overridden, and keep unchanged.

If option value ```mongodb``` or ```memcached``` are set to ```None``` (by default), then
```stack.kubernetesdefaultdomain``` is used to complete the FQDN of ```mongodb``` and ```memcached``` servers name.
This value is concatenated to the server hostname.

| Hostname         | FQDN |
|--------------------|-------------|
|  ```mongodb```  | ```mongodb.abcdesktop.svc.cluster.local```   |
|  ```memcached```  |  ```memcached.abcdesktop.svc.cluster.local```  | 

The dns resolution need a running ```core-dns```is the namespace ```kube-system```

```stack.kubernetesdefaultdomain``` is used also if ```desktop.desktopuseinternalfqdn: True ```

The pod name FQDN is built using the ```$podid```.desktop.```$stack.kubernetesdefaultdomain```

For example, by default :

```c8c7d38f-7621-40bb-a777-83f41b32733e.desktop.abcdesktop.svc.cluster.local```




# How to do the labs and exercices

abcdesktop labs and tutorials are written using a desktop host. The supported operating system are :


| Operating System   | Recommended version   |
|--------------------|-------------|
|  ```GNU/Linux```   | Ubuntu 18.04.4 LTS (Bionic Beaver)  |
|  ```macOS/X``` | Catalina version 10.15.3 (and above)| 
|  ```Windows 10```  | Version 1703 (and above) |


## Choose ```desktop``` or ```server```

* If you choose ```server```, please translate the ```URL``` request ```http://localhost``` with the hostname of your server. 

For example, if you are doing the exercice on a hostname 'server01.labs.domain.local', you have to translate the ```URL``` request ```http://localhost``` with  ```http://server01.labs.domain.local```

> Your web browser (**like Google Chrome**) may refuse unsecure websocket (ws) connections to localhost or your FQDN (only wss, so you should setup a TLS certificate for your local web/websocket server). It should work without any issues in **Mozilla Firefox** on localhost.


* If you choose ```desktop```, the ```URL``` request ```http://localhost``` will reach your local services.

# Setup applications for abcdesktop

Each application is a docker container, to install new docker container run the docker pull command :

Install LibreOffice Suite 

```
docker pull abcdesktopio/base.d
docker pull abcdesktopio/calc.d
docker pull abcdesktopio/impress.d
docker pull abcdesktopio/math.d
docker pull abcdesktopio/writer.d 
```

Install Mozilla Suite 

```
docker pull abcdesktopio/firefox.d
docker pull abcdesktopio/thunderbird.d
```

Install Gnome games 

```
docker pull abcdesktopio/mines.d
docker pull abcdesktopio/tetravex.d
```

Install Gnome tools 

```
docker pull abcdesktopio/calculator.d
docker pull abcdesktopio/terminal.d
```


## Update the cache application list 

The API server does not know that new docker images has been downloaded.  
You have to send a message to the API server, to update the API Server images cache list.

Using your browser or a curl command, call a http request to notify the API Server

```	
http://localhost:30443/API/manager/buildapplist
```

This http request returns a json object, with all docker images details. This json file contains all this docker image installed on the host.

![buildapplist json format](img/json-image-list.png)

Now reconnect to your abcdesktop. 
Open your navigator to http://[your-ip-hostname]:30443/

```	
http://localhost:30443/
```

The new application are installed, and ready to run.
 


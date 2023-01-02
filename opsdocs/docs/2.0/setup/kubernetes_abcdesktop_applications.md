
# Setup applications for abcdesktop

Each application is a docker container, to install new docker container run the docker pull command :

Install LibreOffice Suite 

```
docker pull abcdesktopio/base.d:2.0
docker pull abcdesktopio/calc.d:2.0
docker pull abcdesktopio/impress.d:2.0
docker pull abcdesktopio/math.d:2.0
docker pull abcdesktopio/writer.d:2.0
```

Install Mozilla Suite 

```
docker pull abcdesktopio/firefox.d:2.0
docker pull abcdesktopio/thunderbird.d:2.0
```

Install Gnome games 

```
docker pull abcdesktopio/mines.d:2.0
docker pull abcdesktopio/tetravex.d:2.0
```

Install Gnome tools 

```
docker pull abcdesktopio/calculator.d:2.0
docker pull abcdesktopio/terminal.d:2.0
```


## Connect to your abcdesktop

The API server receives a new image event from docker daemon. To run the new applications just refresh you web browser page.

Now reconnect to your abcdesktop. 

Open your navigator to http://[your-ip-hostname]:30443/

```	
http://localhost:30443/
```

The new applications are installed, and ready to run.
 


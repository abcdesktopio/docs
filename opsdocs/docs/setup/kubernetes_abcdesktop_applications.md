
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


## Connect to your abcdesktop

The API server receives a new image event from docker daemon. To run the new applications just refresh you web browser page.

Now reconnect to your abcdesktop. 

Open your navigator to http://[your-ip-hostname]:30443/

```	
http://localhost:30443/
```

The new applications are installed, and ready to run.
 


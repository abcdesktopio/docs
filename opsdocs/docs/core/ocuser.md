# The POD User

After the login process, if no associated pod is all ready running, a new user pod is started.
This pod starts at least a container with the graphical image.


## Inside the POD User

![Inside a pod](/img/insidepod.png)

The pod user runs by default a container with the graphical image : the oc.user.18.04.

A pod can also runs sound container image, and a printer container.
These options are defined in the [od.config](/config/desktop/) configuration file [ section ```desktop.soundimage``` and ```desktop.printerimage```].



## Processes running inside the user container

All processes are running as the user named ```balloon```, because none of theme need to run as ```root```.

The userid and the guid are ```4096```. 

### Supervisord

[Supervisor](http://supervisord.org) is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.
All process running inside the user container, are started by supervisord. 

```
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
```

Supervisor is the parent of all running process

```
docker-entrypoi---supervisord-+-Xvnc
                              |-node---10*[{node}]
                              |-4*[nodejs---10*[{nodejs}]]
                              |-nodejs---6*[{nodejs}]
                              |-nodejs-+-bash---pstree
                              |        `-11*[{nodejs}]
                              |-openbox
                              `-xsettingsd
```





## TigerVNC Xvnc

[TigerVNC](https://tigervnc.org/) is a high-performance, platform-neutral implementation of ```VNC``` (```Virtual Network Computing```), a client/server application that allows users to launch and interact with graphical applications on remote machines. [TigerVNC](https://tigervnc.org/) provides the levels of performance necessary to run 3D and video applications, and it attempts to maintain a common look and feel and re-use components, where possible, across the various platforms that it supports. [TigerVNC](https://tigervnc.org/) also provides extensions for advanced authentication methods and TLS encryption.

Starts parameters 

```
command=Xvnc :0 -geometry 3840x2160 -SendPrimary=0 -depth 24 -rfbunixpath /tmp/.x11vnc -pn -rfbauth /composer/run/.vnc/passwd```
```  

The default DISPLAY is :0. 
```Xvnc``` listen on unix socket file ```/tmp/.x11vnc```. 

## Openbox 

[Openbox](http://openbox.org/) is the window manager, it supports extensive standards support.

Openbox is [patched with few line](https://github.com/abcdesktopio/openbox) to send ```SIG_USR1``` and ```SIG_USR2``` messages to internal spawner service. 
This patch is only required to send message (Create/Close) to the abcdesktop.io web front.

This patch add notification when X11/window change :

The notify patch send signals SIGUSR1 and SIGUSR2 to a process (pid)

```
#define SIG_MANAGED_WINDOW   SIGUSR1
#define SIG_UNMANAGED_WINDOW SIGUSR2
```

- SIGUSR1: when a new window is created
- SIGUSR2: when a window is closed



Openbox is started by supervisord using the command :

```
command=/usr/bin/openbox --sm-disable --config-file /etc/X11/openbox/rc.xml --startup /composer/openbox/autostart.sh
```


## ws-tcp-bridge

[ws-tcp-bridge](https://github.com/andrewchambers/ws-tcp-bridge) A websocket to tcp proxy server, using nodejs which bridges websockets and tcp servers in either direction.

ws-tcp-bridge is started by supervisord using the command :

```
/composer/node/ws-tcp-bridge/ws-tcp-bridge --method=ws2tcp --lport 6081 --rhost=unix:/tmp/.x11vnc
```

## Spawner-service.js

spawner-service.js is a daemon written in nodejs, this daemon listen for messages on the tcp port 8001.
spawner-service offers methods to interact with the container and the X11 server : 

- launch: start a new application inside the container [ use for builtin applications ]
- filesearch: search file by keywords
- activate: activate a window
- raise: raise a window
- minimize: minimize a window
- close: close a window
- getwindowslist: get window list
- activatewindow: activate a window
- closewindow
- minimizewindow
- raisewindow
- info: get container information 
- clipboardsync: Sync primary clipboard to gtk default clipboard
- getbroadcastwindowslist: broadcast the window list to all connected users
- getappforfile: get the application key for a filename 
- getmimeforfile: get the mime type for a filename
- echo: return an echo string

spawner-service.js is started by supervisord using the command :

```
command=nodejs /composer/node/spawner-service/spawner-service.js
```


## Printer-service.js

Printer-service.js waits for a file in /home/balloon/.printer-queue directory. Printer-service.js use broadcastevent to notify the web browser to download new files to print. 
Printer-service.js is started by supervisord using the command :

```
command=nodejs /composer/node/printer-service/printer-service.js
```

## Broadcast-service.js
Broadcast-service.js allows to broadcast messages between all user sharing the same session.
 
Broadcast-service.js is started by supervisord using the command :

```
command=nodejs /composer/node/broadcast-service/broadcast-service.js
```

## File-service.js

File-service.js is a upload/download service to tranfert files between the browser and the user home directory. File-service.js supports the HTTP method POST to uploadFile and GET to respond data file. File-service.js is used for printer-service.js to download PDF printed files. File-service.js use the tcp port 8080.

```
http.createServer(function(req, res) {
  if (req.method === 'POST') {
	uploadFile( req, res );
  } 
  else if (req.method === 'GET') {
    	respondFile( req, res );
  }
}).listen(8080, function() {
  console.log('Listening for requests');
});
```

File-service.js is started by supervisord using the command :

```
command=nodejs /composer/node/file-service/file-service.js
```

## Pulseaudio
[PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Community/) is a sound system for POSIX, and is a proxy for sound applications. It allows you to do advanced operations on your sound data as it passes between applications. Pulseaudio is use as server to forward sound between X11 applications and the user browser. It supports also virtual local sound. 

file etc/pulse/default.pa
```
load-module module-native-protocol-unix
load-module module-always-sink
load-module module-native-protocol-tcp
```

Pulseaudio is started by supervisord using the command :

```
command=/usr/bin/pulseaudio
```

## Xsettingsd

[Xsettingsd](https://github.com/derat/xsettingsd) is a daemon that implements the XSETTINGS specification. Xsettingsd is use to run GTK+ applications, to configure things such as themes, font antialiasing/hinting, and UI sound effects without we using the GNOME desktop environment.
Xsettingsd set the default GTK theme and color pallette:
```
Net/ThemeName "Numix-Flatstudio"
Net/IconThemeName "Numix-Light"
Gtk/ColorPalette "black:white:gray50:red:purple:blue:light blue:green:yellow:orange:lavender:brown:goldenrod4:dodger blue:pink:light green:gray10:gray30:gray75:gray90"
```

Xsettingsd is started by supervisord using the command.

```
command=/usr/bin/xsettingsd -c /home/balloon/.xsettings
```

## Build the user container image

The image oc.user.18.04 is based from the oc.software.18.04 witch came from oc.ubuntu.18.04.

```
+-------------------+
| oc.user.18.04     |		(abcdesktop.io custom software component)
+---------+---------+
          |
+---------+---------+
| oc.software.18.04 |		(abcdesktop.io ubuntu software component)
+---------+---------+
          |
+---------+---------+
| oc.ubuntu.18.04   |		(abcdesktop.io ubuntu service)
+-------------------+
          |
+---------+---------+
|   ubuntu:18.04    | 		(official ubuntu images from dockerhub)
+-------------------+
```

To build the image oc.user container from scratch, you need to build there 3 images. Build oc.ubuntu.18.04 first, next oc.software.18.04, and finish by oc.user.18.04.
This is done by the Makefile command.

```
docker build -t oc.ubuntu.18.04 -f oc.ubuntu.18.04 .
docker build -t oc.software.18.04 -f oc.software.18.04 .
docker build -t oc.user.18.04	-f oc.user.18.04 .
```

To do it automaticly, clone composer/dockerbuild and run the Makefile

```
git clone https://github.com/abcdesktopio/oc.user.18.04.git 
make
```

### Dockerfile oc.ubuntu.18.04
oc.ubuntu.18.04 is a Dockerfile, it starts 'FROM ubuntu:18.04' and  installs core services and libs:

- nodejs: use by services
- tiger VNC: X11 server	
- supervisor: service manager
- xsettingsd: for X11 params
- pulseaudio: fo sound 
- openbox: the windows manager
- cups and cups-pdf: for printing support

### Dockerfile oc.software.18.04
oc.software.18.04 is a Dockerfile, it starts 'FROM oc.ubuntu.18.04' and installs software components:

- gnome-terminal
- xclip

### Dockerfile oc.user.18.04
oc.user.18.04 is a Dockerfile, it starts 'FROM oc.software.18.04' and installs user software components:

#### Install nodejs dev
```
# Add nodejs service
RUN cd /composer/node/broadcast-service         && npm install  \
	&& cd /composer/node/file-service              && npm install  \
	&& cd /composer/node/printer-service           && npm install  \
	&& cd /composer/node/spawner-service           && npm install  \
	&& cd /composer/node/spawner-service/node_modules/geoip-lite && npm run-script updatedb \
	&& cd /composer/node/angular-filemanager-nodejs-bridge && npm install 
RUN cd /composer/node/livesound-service 		&& npm install
```

#### Create the balloon user

```
RUN groupadd --gid 4096 $BUSER
RUN useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups lpadmin,sudo $BUSER
```

#### Change default permission to run cupsd
```
# change acces right for printer support
RUN addgroup $BUSER lpadmin
RUN mkdir /var/run/cups 
RUN 	chown -R $BUSER:$BUSER /var/spool/cups 		&& \
    	chown -R $BUSER:$BUSER /var/spool/cups-pdf 	&& \
	chown -R $BUSER:$BUSER /var/log/cups		&& \
	chown -R $BUSER:$BUSER /var/cache/cups          && \
	chown -R $BUSER:$BUSER /etc/cups/printers.conf  && \
	chown -R $BUSER:$BUSER /var/run/cups/
```

#### Set the exposed tcp port


Datas to these tcp ports are routed by [nginx](nginx.md)

```
PULSEAUDIO_HTTP_PORT 				4714
WS_TCP_BRIDGE_SERVICE_TCP_PORT		6081
RESERVED_FOR_NEXT_VERSION			29780
XTERM_TCP_PORT 						29781
FILE_SERVICE_TCP_PORT 				29783
BROADCAST_SERVICE_TCP_PORT 			29784
RESERVED FOR CUPSD 					29785
SPAWNER_SERVICE_TCP_PORT 			29786
```

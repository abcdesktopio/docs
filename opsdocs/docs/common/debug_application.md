# How to debug containerised application

## Requirements 

* abcdesktop ready to run
* `docker` or `ctr` package should be install on your Linux (optional)


## Goals

* Read log from web interface
* Read log from daemon interface (optionnal)
* Read stdout and stderr, dump all environment variables, and entrypoint log, to troubleshoot application error and get quick informations


## Read log from web interface

Start an containerised application, I choose `2048` application, for example.

![start 2048 application](img/debug-application-start-2048.png )

Using the web browser, choose `Settings` in the menu.

![menu settings](img/debug-application-settings-menu.png )

Choose `Tasks` to list all running containers

![](img/debug-application-task-web-interface.png)

Choose `Logs` to read the stdout log file of an application

![](img/debug-application-log-web-interface.png)

This application write on `stdout`

```
Error setting cipher RC4
40F7D1D5D07F0000:error:0308010C:digital envelope routines:inner_evp_generic_fetch:unsupported:../crypto/evp/evp_fetch.c:349:Global default library context, Algorithm (RC4 : 37), Properties ()
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-balloon'
qml: Started a new game
```

## Read log from daemon interface (optionnal)

You will read the sample stdout line, using a `docker logs` command, open a shell on you host.

In a shell on your host, look for the `container id` of the `2048` containerised application

```bash
$ docker ps -a|grep 2048
01579054a1f6   abcdesktopio/ubuntu-2048.d:3.0   "/composer/appli-doc…"   21 minutes ago     Up 21 minutes                                                                   anonymous-ubuntu-2048-37830ad00d9f473aa4d0c7872089c6b8
```

Read the log file form the `docker logs` command

```bash
$ docker logs 01579054a1f6
```

You should read on output the same lines written on the web interface

```
Error setting cipher RC4
40F7D1D5D07F0000:error:0308010C:digital envelope routines:inner_evp_generic_fetch:unsupported:../crypto/evp/evp_fetch.c:349:Global default library context, Algorithm (RC4 : 37), Properties ()
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-balloon'
qml: Started a new game
```



## Read log files from an application using the redirected `stderr` and `stdout`


The main log files are `lastcmd.log` `lastcmdenv.log` and `$APPBIN.log`:

- `/tmp/lastcmd.log` : contains the stdout file of the init script command `/composer/appli-docker-entrypoint.sh` for latest running application
- `/tmp/lastcmdenv.log`: contains the dump of all environment variables for latest running application
- `/tmp/$APPBIN.log`: contains `stderr` and `stdout` of the application `$APPBIN`. `$APPBIN` should be replace by the name of your binary application filename.


By default, with all abcdesktop templates, applications redirect `stderr` to `stdout` and pipe to a tee.


```
${APP} ${ARGS} "${APPARGS}" 2>&1 | tee /tmp/$BASENAME_APP.log
```

By default, the `/tmp` volume is shared with all containers.
So to debug and read log applications, you can run a `webshell` to have an access to `stdout` and `stderr` content.

The var `$BASENAME_APP` is the name of your application

```
BASENAME_APP=$(basename "$APPBIN")
```

and `APPBIN` is `path` to the binary

Example with the `2048-qt` application

```
APPBIN=/usr/games/2048-qt
```

![application log](img/debug-application.png)

The `/tmp` directory, you can read the log file '/tmp/2048-qt.log'. Look at the `/tmp` directory

```
balloon:~$ ls -la /tmp/
total 20
drwxrwxrwt 5 root    root     260 Dec  1 09:58 .
drwxr-xr-x 1 root    root    4096 Dec  1 09:55 ..
-rw-r--r-- 1 balloon balloon  102 Dec  1 09:58 2048-qt.log
srwxrwxrwx 1 root    root       0 Dec  1 09:55 .cups.sock
-rw-r--r-- 1 balloon balloon    0 Dec  1 09:57 gnome-2048.log
-rw-r--r-- 1 balloon balloon 1175 Dec  1 09:58 lastcmdenv.log
-rw-r--r-- 1 balloon balloon  437 Dec  1 09:58 lastcmd.log
drwx------ 2 balloon balloon   60 Dec  1 09:55 pulse-jkzlygT9Y7lT
srwxrwxrwx 1 balloon balloon    0 Dec  1 09:55 .pulse.sock
drwx------ 2 balloon balloon   40 Dec  1 09:58 runtime-balloon
-r--r--r-- 1 balloon balloon   11 Dec  1 09:55 .X0-lock
drwxrwxrwt 2 root    root      60 Dec  1 09:55 .X11-unix
srw------- 1 balloon balloon    0 Dec  1 09:55 .x11vnc
balloon:~$
```

The files are `/tmp/lastcmd.log`, `/tmp/lastcmdenv.log` and  `/tmp/2048-qt.log`.

- `/tmp/lastcmd.log` the init command log file created by  `/composer/appli-docker-entrypoint.sh`
- `/tmp/lastcmdenv.log` the last environment variables file
- `/tmp/2048-qt.log` the command log file for the application


Dump the `/tmp/2048-qt.log`, with a cat command `cat /tmp/2048-qt.log`. Replace `/tmp/2048-qt.log` by your own application (binary) if you choose another application.

You can run all bash commands inside the `webshell`.


```
balloon:~$ cat /tmp/2048-qt.log 
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-balloon'
qml: Started a new game
```


Dump the `/composer/appli-docker-entrypoint.sh` result in `/tmp/lastcmd.log`, with a cat command `cat /tmp/lastcmd.log`.


```
balloon:~$ cat /tmp/lastcmd.log 
APP=/usr/bin/gnome-2048
ARGS=
APPARGS=
run previous init overlay stack
run init app if exists
BASENAME_APP=gnome-2048
xauth add :0.0 MIT-MAGIC-COOKIE-1 55dd9838e9404e3b13b635153365d3
setting pulseaudio cookie
end of app exit_code=0
```

Dump all environment variables in file `/tmp/lastcmdenv.log`.

```
balloon:/tmp$ cat /tmp/lastcmdenv.log 
BUSER=balloon
SENDCUTTEXT=enabled
PARENT_ID=2eecb67f5408c2552e7ee78b4fa2c9a419e9af9557c12c4d2f9f5c4fd1af70f4
APPBIN=/usr/games/2048-qt
HOSTNAME=c477d8983486
LANGUAGE=en_US
STDOUT_LOGFILE=/tmp/lastcmd.log
LC_ADDRESS=en_US.UTF-8
CUPS_SERVER=/tmp/.cups.sock
LIBOVERLAY_SCROLLBAR=0
LC_MONETARY=en_US.UTF-8
PULSEAUDIO_COOKIE=17de4db317fbf10624911dbe28c528bd
PWD=/home/balloon
LOGNAME=balloon
XAUTH_KEY=55dd9838e9404e3b13b635153365d3
TZ=Europe/Paris
HOME=/home/balloon
LC_PAPER=en_US.UTF-8
LANG=en_US.UTF-8
ACCEPTCUTTEXT=enabled
APP=/usr/games/2048-qt
APPNAME=ubuntu-2048
DEBCONF_FRONTEND=noninteractive
SET_DEFAULT_WALLPAPER=welcometoabcdesktop.png
TERM=linux
LC_IDENTIFICATION=en_US.UTF-8
USER=balloon
DISPLAY=:0.0
SHLVL=1
LC_TELEPHONE=en_US.UTF-8
LC_MEASUREMENT=en_US.UTF-8
UBUNTU_MENUPROXY=0
STDOUT_ENVLOGFILE=/tmp/lastcmdenv.log
BROADCAST_COOKIE=b7bc93457df5aa6bedb5ad2fe972268fa268bf3439b4024c
LC_TIME=en_US.UTF-8
LC_ALL=en_US.UTF-8
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PULSE_SERVER=/tmp/.pulse.sock
LC_NUMERIC=en_US.UTF-8
```

We describe how to read the environment variables, the stdout file and the stderr file, to get some information and error for a containerised application.

In [next chapter](debug_application_create) we will start an application from a fresh ubuntu image, to get more details.

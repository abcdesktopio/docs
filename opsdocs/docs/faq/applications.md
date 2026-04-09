---
tags:
  - faq
  - applications
  - (JFV) propositions de maj
---

**[JFV] Attention, il y a maintenant lce qui sera le plus évident pour l'ajoute d'aplication à l'unité: le mode web via la console**

# FAQ applications

## How to delete all applications ?


To delete all applications use the images endpoint, replace `localhost:30443` by your own datas

```bash
curl -X DELETE -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/images/
```

It returns a json list of all deleted applications

```json
["abcdesktopio/2048-alpine.d:3.0", "abcdesktopio/2048-ubuntu.d:3.0", "abcdesktopio/apachedirectorystudio.d:3.0", "abcdesktopio/astromenace.d:3.0", "abcdesktopio/base.d:3.0", "abcdesktopio/beekeeperstudio.d:3.0", "abcdesktopio/blender.d:3.0", "abcdesktopio/bless.d:3.0", "abcdesktopio/blobby.d:3.0", "abcdesktopio/boxes.d:3.0", "abcdesktopio/calculator.d:3.0", "abcdesktopio/chess.d:3.0", "abcdesktopio/chimerax.d:dev", "abcdesktopio/chrome.d:3.0", "abcdesktopio/chromium.d:3.0", "abcdesktopio/citrix.d:3.0", "abcdesktopio/cloudfoundry.d:3.0", "abcdesktopio/cmd.exe.d:3.0", "abcdesktopio/corsix-th.d:3.0", "abcdesktopio/cuda.d:dev"]
```

## How to add an application ?

To add an application :
- get the json file of an application
- push the json file to the abcdesktop's images endpoint


```bash
wget https://raw.githubusercontent.com/abcdesktopio/oc.apps/main/2048-alpine.d.3.0.json
curl -X POST -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/image -d @2048-alpine.d.3.0.json
```

The first start will pull the 2048 image, so it can take a while.


## How to get the json file of a containerized application ?

To get the json file of a containerized application, you can use `docker` command or `crictl` command

- `docker` command

```bash
docker inspect abcdesktopio/2048-alpine.d:3.0 > 2048-alpine.json
```

- `crictl` command

```bash
crictl inspecti abcdesktopio/2048-alpine.d:3.0 > 2048-alpine.json
```


## My application doesn't start. How to get log files ?

Open the `webshell` and read the logs files.

The log files are /tmp/lastcmd.log, /tmp/lastcmdenv.log and /tmp/NAME OF THE APPLICATION.log.

- `/tmp/lastcmd.log` the init command log file created by /composer/appli-docker-entrypoint.sh
- `/tmp/lastcmdenv.log` the last environment variables file
- `/tmp/NAME OF THE APPLICATION.log` the command log file for the application



# desktop.pod

abcdesktop defines a user desktop as a pod (a group of containers). This is a main features of abcdesktop.
Each container offers a service. For example 

- `printer` is a container. `printer` service runs inside the user pod, it can be started or not. 
- `graphical` is a container. `graphical` service runs inside the user pod.


## containers in the user pod

- `init` contains init command for user pod
- `graphical` is the user graphical service (X11 and VNC)
- `printer` is the printer service (cupsd)
- `sound` is the sound service (pulseaudio)
- `filer` is the filer service to upload and download file into the user home directory


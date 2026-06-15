# desktop.pod

abcdesktop represents each user desktop as a Kubernetes pod — a group of containers. This is a core feature of abcdesktop. Each container provides a dedicated service. For example:

- `printer` is a container. `printer` service runs inside the user pod, it can be started or not. 
- `graphical` is a container. `graphical` service runs inside the user pod.


## containers in the user pod

- `init` runs the initialization commands for the user pod
- `graphical` is the user graphical service (X11 and VNC)
- `printer` is the printer service (cupsd)
- `sound` is the sound service (PulseAudio)
- `filer` is the file transfer service for uploading and downloading files to and from the user's home directory

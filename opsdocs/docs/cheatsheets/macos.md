Docker For Mac embeds a hypervisor (based on [xhyve](https://github.com/machyve/xhyve)), a Linux distribution which runs on LinuxKit and filesystem & network sharing that is much more Mac native. Docker For Mac is a Mac native application in /Applications. 

At installation time, it creates symlinks in /usr/local/bin for docker and docker-compose, to the commands in the application bundle, in /Applications/Docker.app/Contents/Resources/bin.

To install dockerd on MacOS/X, use Docker for Desktop. Get Docker for MacOS on the docker website 
[docker-for-mac](https://docs.docker.com/docker-for-mac/)

To get a shell to the `LinuxKit docker-desktop`, run the docker command 

```
docker run -it --rm --privileged --pid=host justincormack/nsenter1
```

> more info: [https://github.com/justincormack/nsenter1](https://github.com/justincormack/nsenter1)



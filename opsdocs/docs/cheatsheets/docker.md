# Docker scripting cheatsheets

## Common Docker commands

### update all images

```
docker images |grep -v REPOSITORY|awk '{print $1}'|xargs -L1 docker pull
```

### Remove exited container

```
docker rm `docker ps -a -q -f "status=exited"`
```

### Remove dangling images

```
docker rmi `docker images -q --filter "dangling=true"`
```

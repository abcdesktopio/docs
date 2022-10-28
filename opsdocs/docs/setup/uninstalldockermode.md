# Uninstall abcdesktop.io for non-cluster hosts

## Commands to uninstall abcdesktop.io 

Go to the abcdesktop directory (where the `docker-compose.yml` is located), and run the bash commands  : 

```bash
echo "starting abcdesktop uninstall commands"
docker-compose -p abcdesktop down
echo "stop and remove abcdesktop services"
docker-compose rm -s -v -f
echo "remove all abcdesktop user container"
docker ps --filter "label=type=x11server" -q | xargs docker stop
docker ps --filter "label=type=x11server" -q | xargs docker rm
echo "remove all abcdesktop images"
docker images --filter=reference='abcdesktopio/*:*' --format "{{.Repository}}"  | xargs docker rmi
echo "remove all user volumes"
docker volume ls -f label=type=x11server -q | xargs docker volume rm
echo "abcdesktop is uninstalled"
```

Great, you have uninstalled abcdesktop in non-cluster hosts.


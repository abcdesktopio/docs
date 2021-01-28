
# abcdesktop overview

abcdesktop is based on docker, from the service infrastructure to the user applications.
At the login page, the user chooses a login provider and authenticates himself, then abcdesktop engine creates a graphical user container. 



![abcdesktop Architecture overview](img/architecture-overview.png)


### abcdesktop services
- **nginx**     : container act as static web server and reverse proxy router
- **pyos**      : container abcdesktop core engine
- memcached : container cache service
- mongo     : container database service to store user profil information

### abcdesktop User
- **user**   : user container, one container per connected user
- **applications** : each graphical application runs inside a dedicated container. You need to create an docker image for each application



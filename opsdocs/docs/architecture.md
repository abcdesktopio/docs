# Architecture in docker mode


## abcdesktop workflow (with LDAP Auth)


![Create POD process](img/createPod.png)

1. User login, get a user JWT
2. Create a user POD (or a container) and retrieve a Desktop JWT
3. Run, the user is connected to his own POD (or container)

	- All JWT are signed with RSA keys. 
	- All JWT payload are encrypted with RSA keys

## Services Infrastructure

The service infrastructure is based on :

- WebServer [Nginx container](/core/nginx)
- Database service [MongoDB](/core/mongodb/)
- Memcached service [Memcached](/core/memcached/)
- Pyos Core service (abcdesktop engine) [Pyos](/core/pyos/)

The user creates a pod [user](/core/user)


## Roles summary

### pyos

`pyos` is the core abcdesktop service act as a control plane. Pyos is a stateless services, Pyos's roles are :

- Authenticate user on authenticate providers
 - OAuth 2.0 Provider : Google, Facebook, Orange
 - LDAP and LDAPS
 - Active Directory
- Start/Stop user container in docker mode and Pod in Kubernetes mode 
- Start/Stop application container

When a new user is authenticated, a dedicated user container is created. 
When the user starts an application (like LibreOffice for example) a dedicated application container is created.

### nginx

`nginx` container act as web server and websocket reverse proxy. 

### mongo
`mongo` is used by pyos to store user profil informations. 
The profil informations are :

- Login history
- Dock configuration
- Image and background color configuration 


### memcached
`memcache` stores progress text message information during login process. `memcache` datas are set and get only by the control plane.


### oc.user
[`oc.user`](https://github.com/abcdesktopio/oc.user) is the name of the user's container image. `oc.user` runs the X11 graphical service. `oc.user` is based on ubuntu distribution. 

* The image `abcdesktopio/oc.user.ubuntu:3.0` is based on `ubuntu` distribution `22.04`. Get more details about [oc.user](https://github.com/abcdesktopio/oc.user) image.


### applications
All applications are containers or pods, and share a graphical socket with the user's container 

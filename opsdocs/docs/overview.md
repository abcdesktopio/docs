
# abcdesktop overview

abcdesktop is based on kubernets, from the abcdesktop infrastructure to the user applications.
At the login page, the user chooses a login provider and authenticates himself, then abcdesktop engine creates a user pod.

## abcdesktop design

![abcdesktop Architecture overview](img/architecture-overview.png)


### abcdesktop services
* nginx : container act as static web server and reverse proxy router
* pyos  : container abcdesktop core control plane
* memcached : container cache service
* mongo     : container database service to store user profil information

### abcdesktop pod user
* user: pod user, one pod per connected user
* applications : each graphical application runs inside a dedicated container. You need to create an container image for each application

## applications

* An application can run as ephemeral container or as pod, it MUST be a container.
* An application can ask to start another container, like application helper for a web browser. By example, Firefox container can ask to start videolan application. Then Firefox is running inside a container, Videolan is running inside another separated container. abcdesktop manages a mimetype database for each user. The mimetype database is updated on the fly then new application is added.
* Application resource limit is supported (CPU, memory).
* The share memory (shm) between X.org and application is supported with the ephemral container.
* An application can use GPU if need.
* Application support ACL (Access Control List). Access to an application can be allowed for a user and denied for another one, using group membership for example.
* Volumes can be mounted for an application or not for security reason.
* Application can bind a dedicated network such as VLAN.

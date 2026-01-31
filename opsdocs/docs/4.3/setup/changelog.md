# Change log from 4.2 to 4.3


The prominent changes for this release are:

* remove endpoints resources 
* Migration from mongo:4.4 to mongo:8.0 safe
* Add replicaset `rs0` support for mongodb
* Add `tigervncserver 1.16.0`
* Add support of libnss-extrausers for `passwd`, `group` and `shadow` files, for `oc.user` container and for all applications.
  * default `passwd`, `group`, `shadow` and `gshadow` are NOT updated anymore. The new user are provisioned in `/var/lib/extrausers`
  > No need to define symbolic link to `passwd`, `group`, `shadow` and `gshadow` any more
  * fix the issue `containerd container: mount callback failed on /var/lib/containerd/tmpmounts/containerd-mount1487488778: openat etc/passwd: path escapes from parent`
* Add support for application for distributions
  * `alpine` (without extrausers support)
  * `debian` (with extrausers support)
  * `ubuntu` (with extrausers support)
  * `rockylinux` (Red Hat®) (with extrausers support from [libnss-extrausers-rpm](https://github.com/abcdesktopio/libnss-extrausers-rpm))
  > For example you can add firefox from alpine, and firefox from debian, and firefox from ubuntu, and firefox from rockylinux in the same desktop
* Add new volumes support in `od.config` file
  * Allow changes for on-premise intregration
 
  Default volumes
  ```python
  'default_volumes': {
    'shm': { 'name': 'shm', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '512Mi' } },
    'run': { 'name': 'run', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi'    } },
    'tmp': { 'name': 'tmp', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'log': { 'name': 'log', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'rundbus': { 'name': 'rundbus',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi' } },
    'runuser': { 'name': 'runuser',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi' } },
    'x11socket': { 'name': 'x11socket',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Ki' } },
    'cupsdsocket': { 'name': 'cupsdsocket',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Ki' } },
    'extrausers': { 'name': 'extrausers',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi' } },
    'sudoers': { 'name': 'sudoers',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi' } }
  },
  ```

  are mounted on `mountPath`
  
  ```python
  'default_volumes_mount': {
    'shm': { 'name': 'shm', 'mountPath' : '/dev/shm' },
    'run': { 'name': 'run',  'mountPath': '/var/run/desktop' },
    'tmp': { 'name': 'tmp',  'mountPath': '/tmp' },
    'log': { 'name': 'log',  'mountPath': '/var/log/desktop' },
    'rundbus': { 'name': 'rundbus',  'mountPath': '/var/run/dbus' },
    'runuser': { 'name': 'runuser',  'mountPath': '/run/user/' },
    'x11socket': { 'name': 'x11socket',  'mountPath': '/tmp/.X11-unix' },
    'pulseaudiosocket':  { 'name': 'pulseaudiosocket',  'mountPath': '/tmp/.pulseaudio' },
    'cupsdsocket': { 'name': 'cupsdsocket',  'mountPath': '/tmp/.cupsd' },
    'extrausers': { 'name': 'extrausers',  'mountPath': '/var/lib/extrausers' },
    'sudoers': { 'name': 'sudoers', 'mountPath': '/etc/sudoers.d' }
  },
  ```     

      

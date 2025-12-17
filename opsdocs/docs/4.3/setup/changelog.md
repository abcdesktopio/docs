# Change log from 4.2 to 4.3


The prominent changes for this release are:

* Migration from mongo:4.4 to mongo:8.0 safe
* Add replicaset `rs0` support for mongodb
* Add support of libnss-extrausers for `passwd`, `group` and `shadow` files, for `oc.user` container and for all applications.
  * default `passwd`, `group`, `shadow` and `gshadow` are NOT updated anymore. The new user are provisioned in `/var/lib/extrausers`
* Add support for application for distributions
  * `alpine` (without extrausers support)
  * `debian` (with extrausers support)
  * `ubuntu` (with extrausers support)
  * `rockylinux` (Red Hat®) (with extrausers support from [libnss-extrausers-rpm](https://github.com/abcdesktopio/libnss-extrausers-rpm))
  > For example you can add firefox from alpine, and firefox from debian, and firefox from ubuntu, and firefox from rockylinux in the same desktop
* Add new volumes support in `od.config` file
  * Allow changes for on-premise intregration
  ```python
  'default_volumes': {
    'uinput'  : { 'name': 'uinput',   'hostPath': { 'path': '/dev/uinput', 'type': 'CharDevice' } },
    'input'   : { 'name': 'input',    'hostPath': { 'path': '/dev/input' } },
    'shm': { 'name': 'shm', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '512Mi' } },
    'run': { 'name': 'run', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1M'    } },
    'tmp': { 'name': 'tmp', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'log': { 'name': 'log', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'rundbus': { 'name': 'rundbus',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8M' } },
    'runuser': { 'name': 'runuser',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8M' } },
    'x11socket': { 'name': 'x11socket',  'emptyDir': { 'medium': 'Memory' } },
    'pulseaudiosocket' :  { 'name': 'pulseaudiosocket',  'emptyDir': { 'medium': 'Memory' } },
    'cupsdsocket': { 'name': 'cupsdsocket',  'emptyDir': { 'medium': 'Memory' } },
    'extrausers': { 'name': 'extrausers',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1M' } },
    'sudoers': { 'name': 'sudoers',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1M' } },
  },
  'default_volumes_mount': {
    'uinput' : { 'name': 'uinput', 'mountPath': '/dev/uinput' },
    'input' :  { 'name': 'input',  'mountPath': '/dev/input'  },
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

      

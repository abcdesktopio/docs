---
title: Desktop Pod secrets
description: Describe auth pod secrets 
keywords: secret, desktop pod, abcdesktop, Kubernetes
tags:
  - desktop
  - secret
---


## About the abcdesktop user's secrets


Then a user login, pyos creates the four secrets `auth-ldif-USER`, `auth-localaccount-USER`, `auth-posixaccount-USER` and `auth-vnc-USER`.

- `auth-ldif-USER` describes datas from LDAP for the current `dn`
- `auth-localaccount-USER` describes informations for `passwd`, `group`, `shadow` and `gshadow` files.
- `auth-posixaccount-USER` describes posix account informations
- `auth-vnc-USER` describes the vnc password

For example when the user `leela` login, pyos creates the four secrets 

- `auth-ldif-leela` 
- `auth-localaccount-leela` 
- `auth-posixaccount-leela`
- `auth-vnc-leela`

```
% kubectl get secrets -n abcdesktop
NAME                          TYPE                      DATA   AGE
abcdesktop-mongod-keyfile     Opaque                    1      11m
abcdesktopjwtdesktoppayload   Opaque                    2      11m
abcdesktopjwtdesktopsigning   Opaque                    2      11m
abcdesktopjwtusersigning      Opaque                    2      11m
auth-ldif-leela               abcdesktop/ldif           18     2m29s
auth-localaccount-leela       abcdesktop/localaccount   14     2m29s
auth-posixaccount-leela       abcdesktop/posixaccount   10     2m29s
auth-vnc-leela                abcdesktop/vnc            1      2m29s
secret-mongodb                Opaque                    7      11m
```

- `auth-ldif-leela` contains the information from the LDAP directory service.

```
% kubectl describe secret auth-ldif-leela -n abcdesktop
Name:         auth-ldif-leela
Namespace:    abcdesktop
Labels:       access_provider=planet
              access_type=ldif
              access_userid=leela
Annotations:  <none>

Type:  abcdesktop/ldif

Data
====
givenName:      5 bytes
homeDirectory:  11 bytes
posix:          524 bytes
uidNumber:      4 bytes
dn:             50 bytes
jpegPhoto:      26526 bytes
name:           13 bytes
userid:         5 bytes
cn:             13 bytes
employeeType:   20 bytes
gidNumber:      5 bytes
mail:           23 bytes
uid:            5 bytes
userPassword:   46 bytes
objectClass:    74 bytes
ou:             15 bytes
sn:             7 bytes
description:    6 bytes
```

- `auth-localaccount-leela` contains to create `passwd`, `group`, `shadow` and `gshadow` files.

```
% kubectl describe secret auth-localaccount-leela -n abcdesktop
Name:         auth-localaccount-leela
Namespace:    abcdesktop
Labels:       access_provider=planet
              access_type=localaccount
              access_userid=leela
Annotations:  <none>

Type:  abcdesktop/localaccount

Data
====
loginShell:     9 bytes
passwd:         44 bytes
shadow:         132 bytes
uid:            5 bytes
uidNumber:      4 bytes
description:    6 bytes
gecos:          2 bytes
gid:            5 bytes
group:          50 bytes
groups:         195 bytes
gshadow:        31 bytes
homeDirectory:  11 bytes
sha512:         106 bytes
gidNumber:      5 bytes
```


- `auth-posixaccount-leela` contains to make a posix account information.

```
% kubectl describe secret auth-posixaccount-leela -n abcdesktop
Name:         auth-posixaccount-leela
Namespace:    abcdesktop
Labels:       access_provider=planet
              access_type=posixaccount
              access_userid=leela
Annotations:  <none>

Type:  abcdesktop/posixaccount

Data
====
gecos:          2 bytes
gid:            5 bytes
homeDirectory:  11 bytes
cn:             5 bytes
gidNumber:      5 bytes
groups:         195 bytes
loginShell:     9 bytes
uid:            5 bytes
uidNumber:      4 bytes
description:    6 bytes
```

- `auth-vnc-leela` contains the vnc password.

```
% kubectl describe secret auth-vnc-leela -n abcdesktop
Name:         auth-vnc-leela
Namespace:    abcdesktop
Labels:       access_provider=planet
              access_type=vnc
              access_userid=leela
Annotations:  <none>

Type:  abcdesktop/vnc

Data
====
password:  15 bytes
```

- If a kubernetes adminisitrator deletes the `vnc secret`, a user can't do a reconnect 

```
kubectl delete secret auth-vnc-leela -n abcdesktop
secret "auth-vnc-leela" deleted
```

You will read on the web interface 

```
Your desktop previous was unreachable. vncpasswod is not defined. Please try to reload again.
```


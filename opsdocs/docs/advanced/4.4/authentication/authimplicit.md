# Authentication `implicit`

## authmanagers `implicit`

The `implicit` provider is the simplest configuration mode and is used for anonymous (always-allow) authentication.

The provider is defined as a dictionary object and contains an `anonymous` provider.

The `anonymous` provider always permits authentication and generates a UUID as the user ID. It is used to bypass the authentication process in demonstration mode.

```
'implicit': {
    'providers': {
      'anonymous': {
        'displayname': 'Guest',
        'textcolor': '#000000',
        'icon': 'img/auth/anonymous_icon.svg',
        'backgroundcolor': '#FFFFFF',
        'caption': 'Have a look !',
        'userid': 'anonymous',
        'username': 'anonymous',
        'policies': { 'acl': { 'permit': [ 'all' ] } }
      }
    }}
```

The `anonymous` provider always permits authentication and generates a UUID as the user ID.

Set the `authmanagers` dictionary in your configuration file as follows:

```
authmanagers: {
  'external': {},
  'explicit': {},
  'implicit': {
    'providers': {
      'anonymous': {
        'displayname': 'Guest',
        'textcolor': '#000000',
        'icon': 'img/auth/anonymous_icon.svg',
        'backgroundcolor': '#FFFFFF',
        'caption': 'Have a look !',
        'userid': 'anonymous',
        'username': 'anonymous',
        'policies': { 'acl': { 'permit': [ 'all' ] } }
      }
    }
  }}
```

[Update your configuration file and apply the new configuration file](../configure/updateconfiguration.md)

Open a new web browser and navigate to your abcdesktop URL. You should see the login page with the Anonymous button:

![login page Anonymous](img/anonymous.png)

Click the `Sign-In Anonymously` button.

You will receive a desktop session as the `anonymous` user.

List all your desktop pods:

```
kubectl get pods -l type=x11server -n abcdesktop
NAME              READY   STATUS    RESTARTS   AGE
anonymous-3806b   3/3     Running   0          9m22s
```

In this example, the pod name is `anonymous-3806b`.

Run a bash shell inside the pod:

```
kubectl exec -it anonymous-3806b -n abcdesktop -- bash
Defaulted container "x-graphical" out of: x-graphical, s-sound, f-filer, i-init (init)
anonymous@abcdesktop:~$ id
uid=4096(anonymous) gid=4096(anonymous) groups=4096(anonymous)
```

The session runs as the `anonymous` user with `uid=4096` and `gid=4096`.


You have successfully verified how the implicit authentication configuration works.

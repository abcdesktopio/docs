# Troubeshooting abcdesktop core services 



## Troubeshooting `nginx` errors 

### Read pod's status

```bash
kubectl get pods -n abcdesktop
NAME                           READY   STATUS             RESTARTS       AGE
memcached-od-78578c879-bb8qq   1/1     Running            0              164m
mongodb-od-5b4dd4765f-ptw2j    1/1     Running            0              164m
nginx-od-788c97cdc9-b4gbq      0/1     CrashLoopBackOff   36 (57s ago)   164m
openldap-od-65759b74dc-tbvfg   1/1     Running            0              164m
pyos-od-7d5d9457cf-jw6nk       1/1     Running            0              164m
speedtest-od-c94b56c88-48cvq   1/1     Running            0              164m
```

The pod `nginx-od-788c97cdc9-b4gbq ` has `CrashLoopBackOff` status. This is wrong.


### Read the pod's log

```bash
kubectl logs -l run=nginx-od -n abcdesktop
```

### Issue with an error in nginx configuration file

```bash
running standart configuration file
starting nginx web server in foreground
nginx: [emerg] unexpected "s" in /etc/nginx/sites-enabled/default:10
```

Nginx has failed to start. There is an error in the configuration file. 

We need to fix the `nginx-config` ConfigMap in the yaml file.


## Start the pod by hands  

If the `kubectl logs` command doesn't return usable information. You can update the pod default command and then start the service by hands.

Update the container description to replace the default command by a sleep command

```yaml
      - name: nginx
        imagePullPolicy: Always
        image: abcdesktopio/oc.nginx:3.1
        command: [ "/usr/bin/sleep" ]
        args: ["1d"]
```

The container will start the command `/usr/bin/sleep` for `1d` (one day).

A default nginx debug pods is available on [https://github.com/abcdesktopio/conf/tree/main/kubernetes/debug](https://github.com/abcdesktopio/conf/tree/main/kubernetes/debug)


```bash
kubectl apply -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/debug/nginx-3.1.yaml
deployment.apps/nginx-od configured
```

Check that nginx pod is `Running`

```bash
kubectl get pods  -l run=nginx-od -n abcdesktop
NAME                       READY   STATUS    RESTARTS   AGE
nginx-od-666df64f4-whtng   1/1     Running   0          2m30s
```

Nginx web service is not started inside the container, only the pod is started. We need to get a shell inside the container to start the nginx web service by hands.

Run the command `/usr/local/openresty/nginx/sbin/nginx -p /etc/nginx -c nginx.conf -e /var/log/nginx/error.log`


```bash
kubectl exec -n abcdesktop -it deployment/nginx-od -- bash
root@nginx-od-666df64f4-whtng:/# /usr/local/openresty/nginx/sbin/nginx -p /etc/nginx -c nginx.conf -e /var/log/nginx/error.log
```

Nginx returns an explicit error, the `/etc/nginx/sites-enabled/default` file is wrong.

```bash
nginx: [emerg] unexpected "s" in /etc/nginx/sites-enabled/default:10
root@nginx-od-666df64f4-whtng:/# 
```

It's time to fix the `nginx-config` ConfigMap in the yaml file.


## Troubeshooting `pyos` errors 


### Read pod's status

```bash
kubectl get pods -n abcdesktop
NAME                            READY   STATUS             RESTARTS      AGE
memcached-od-5ff8844d56-sw9n5   1/1     Running            0             90m
mongodb-od-77c945467d-c47nl     1/1     Running            0             90m
nginx-od-666df64f4-wf99b        1/1     Running            0             22m
openldap-od-5bbdd75864-m6qmh    1/1     Running            0             90m
pyos-od-57946b67c4-m5zc9        0/1     CrashLoopBackOff   5 (17s ago)   3m18s
speedtest-od-7f5484966f-kxkw4   1/1     Running            0             90m
```

The pod `pyos-od-57946b67c4-m5zc9` has `CrashLoopBackOff` status. This is wrong.

### Read the pod's log

```bash
kubectl logs -l run=pyos-od -n abcdesktop
```

```bash
2023-10-15 14:53:00,136 [INFO   ] oc.logging.init_logging: Initializing logging subsystem
2023-10-15 14:53:00,136 [INFO   ] oc.logging.load_config: Reading cherrypy configuration section 'global/logging': path = od.config
2023-10-15 14:53:00,138 [CRITICAL] oc.logging.configure: Failed to configure logging: config_or_path = 'od.config'
Traceback (most recent call last):
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 179, in as_dict
    value = unrepr(value)
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 367, in unrepr
    obj = b.astnode(s)
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 229, in astnode
    p = ast.parse('__tempvalue__ = ' + s)
  File "/usr/lib/python3.8/ast.py", line 47, in parse
    return compile(source, filename, mode, flags,
  File "<unknown>", line 1
    __tempvalue__ = 'abcdesktop
                              ^
SyntaxError: EOL while scanning string literal

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/pyos/oc/logging.py", line 89, in configure
    init_logging(config_or_path, is_cp_file)
  File "/var/pyos/oc/logging.py", line 80, in init_logging
    cfg = config_or_path if isinstance(config_or_path, dict) else load_config(config_or_path, is_cp_file)
  File "/var/pyos/oc/logging.py", line 66, in load_config
    cfg = Config(path)['global']['logging']
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 119, in __init__
    self.update(file)
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 130, in update
    self._apply(Parser.load(config))
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 205, in load
    return Parser().dict_from_file(input) if is_file else input.copy()
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 194, in dict_from_file
    return self.as_dict()
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 185, in as_dict
    raise ValueError(msg, x.__class__.__name__, x.args)
ValueError: ('Config error in section: \'global\', option: \'namespace\', value: "\'abcdesktop". Config values must be valid Python.', 'SyntaxError', ('EOL while scanning string literal', ('<unknown>', 1, 28, "__tempvalue__ = 'abcdesktop\n")))
Failed to load configuration file od.config ('Config error in section: \'global\', option: \'namespace\', value: "\'abcdesktop". Config values must be valid Python.', 'SyntaxError', ('EOL while scanning string literal', ('<unknown>', 1, 28, "__tempvalue__ = 'abcdesktop\n")))
```

It's time to fix the `abcdesktop-config` ConfigMap.
 

## Start the pod by hands  

If the `kubectl logs` command doesn't return usable information. You can update the pod default command and then start the service by hands.

Update the container description to replace the default command by a sleep command

```yaml
      - name : pyos
        imagePullPolicy: Always
        image: abcdesktopio/oc.pyos:3.1
        command: [ "/usr/bin/sleep" ]
        args: ["1d"]
```

The container will start the command `/usr/bin/sleep` for `1d` (one day).

A default nginx debug pods is available on [https://github.com/abcdesktopio/conf/tree/main/kubernetes/debug](https://github.com/abcdesktopio/conf/tree/main/kubernetes/debug)


```bash
kubectl apply -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/debug/pyos-3.1.yaml
deployment.apps/pyos-od configured
```

Check that pyos pod is `Running`

```yaml
kubectl get pods  -l run=pyos-od -n abcdesktop
NAME                       READY   STATUS    RESTARTS   AGE
pyos-od-6cd679d6b8-css9q   1/1     Running   0          5s
```

Pyos service is not started inside the container, only the pod is started. We need to get a shell inside the container to start the pyos service by hands.

Run the command `cd /var/pyos && ./od.py`

```yaml
kubectl exec -n abcdesktop -it deployment/pyos-od -- bash
root@pyos-od-6cd679d6b8-css9q:/var/pyos# cd /var/pyos && ./od.py 
```

`od.py` command returns the same explicit error, the `od.config` file is wrong.

```bash
2023-10-15 14:53:00,136 [INFO   ] oc.logging.init_logging: Initializing logging subsystem
2023-10-15 14:53:00,136 [INFO   ] oc.logging.load_config: Reading cherrypy configuration section 'global/logging': path = od.config
2023-10-15 14:53:00,138 [CRITICAL] oc.logging.configure: Failed to configure logging: config_or_path = 'od.config'
Traceback (most recent call last):
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 179, in as_dict
    value = unrepr(value)
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 367, in unrepr
    obj = b.astnode(s)
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 229, in astnode
    p = ast.parse('__tempvalue__ = ' + s)
  File "/usr/lib/python3.8/ast.py", line 47, in parse
    return compile(source, filename, mode, flags,
  File "<unknown>", line 1
    __tempvalue__ = 'abcdesktop
                              ^
SyntaxError: EOL while scanning string literal

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/pyos/oc/logging.py", line 89, in configure
    init_logging(config_or_path, is_cp_file)
  File "/var/pyos/oc/logging.py", line 80, in init_logging
    cfg = config_or_path if isinstance(config_or_path, dict) else load_config(config_or_path, is_cp_file)
  File "/var/pyos/oc/logging.py", line 66, in load_config
    cfg = Config(path)['global']['logging']
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 119, in __init__
    self.update(file)
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 130, in update
    self._apply(Parser.load(config))
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 205, in load
    return Parser().dict_from_file(input) if is_file else input.copy()
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 194, in dict_from_file
    return self.as_dict()
  File "/usr/local/lib/python3.8/dist-packages/cherrypy/lib/reprconf.py", line 185, in as_dict
    raise ValueError(msg, x.__class__.__name__, x.args)
ValueError: ('Config error in section: \'global\', option: \'namespace\', value: "\'abcdesktop". Config values must be valid Python.', 'SyntaxError', ('EOL while scanning string literal', ('<unknown>', 1, 28, "__tempvalue__ = 'abcdesktop\n")))
Failed to load configuration file od.config ('Config error in section: \'global\', option: \'namespace\', value: "\'abcdesktop". Config values must be valid Python.', 'SyntaxError', ('EOL while scanning string literal', ('<unknown>', 1, 28, "__tempvalue__ = 'abcdesktop\n")))
```

We need to fix the `abcdesktop-config` ConfigMap in the yaml file.

```bash
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config -o yaml --dry-run=client | kubectl replace -n abcdesktop -f -
```





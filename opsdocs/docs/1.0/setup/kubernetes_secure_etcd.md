# Secure Etcd secrets database

>
> This chapter is optional 
> you can skip it if you think that's your kubernetes etcd database access is secured.
> 



Etcd secrets database is the place where all k8s secrets are stored.
By default secrets are stored in plain text. 
If an attacker can access Etcd database, he know then all your secrets.


To secure secrets, we will crypt them at API server level.
All secrets will be stored encrypted in Etcd and then be uncrypted at API server level when accessed by Kubernetes.

## Availbale Encryption Providers

Here are officials available encryption providers ([Kubernetes Official page](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) ):

<table><caption style="display:none">Providers for Kubernetes encryption at rest</caption><thead><tr><th>Name</th><th>Encryption</th><th>Strength</th><th>Speed</th><th>Key Length</th><th>Other Considerations</th></tr></thead><tbody><tr><td><code>identity</code></td><td>None</td><td>N/A</td><td>N/A</td><td>N/A</td><td>Resources written as-is without encryption. When set as the first provider, the resource will be decrypted as new values are written.</td></tr><tr><td><code>aescbc</code></td><td>AES-CBC with PKCS#7 padding</td><td>Strongest</td><td>Fast</td><td>32-byte</td><td>The recommended choice for encryption at rest but may be slightly slower than <code>secretbox</code>.</td></tr><tr><td><code>secretbox</code></td><td>XSalsa20 and Poly1305</td><td>Strong</td><td>Faster</td><td>32-byte</td><td>A newer standard and may not be considered acceptable in environments that require high levels of review.</td></tr><tr><td><code>aesgcm</code></td><td>AES-GCM with random nonce</td><td>Must be rotated every 200k writes</td><td>Fastest</td><td>16, 24, or 32-byte</td><td>Is not recommended for use except when an automated key rotation scheme is implemented.</td></tr><tr><td><code>kms</code></td><td>Uses envelope encryption scheme: Data is encrypted by data encryption keys (DEKs) using AES-CBC with PKCS#7 padding, DEKs are encrypted by key encryption keys (KEKs) according to configuration in Key Management Service (KMS)</td><td>Strongest</td><td>Fast</td><td>32-bytes</td><td>The recommended choice for using a third party tool for key management. Simplifies key rotation, with a new DEK generated for each encryption, and KEK rotation controlled by the user. </td></tr></tbody></table>




aesgcm provider seem's a bit complex to be used.  
kms provider needs to use a dedicated container and will not work out of the box.  
For abcdesktop we will use aescbc provider

## aescbc encryption configuration

### create configuration directory
In  ```/etc/kubernetes``` directory, create a directory named aescbc:
```
sudo mkdir /etc/kubernetes/aescbc
```

### Create configuration file
Create aescbc yaml configuration file:
```
sudo vi /etc/kubernetes/aescbc/encrypt_config.yaml
```
```
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:
        keys:
        - name: key1
          secret: vKZm8oL19mucMS8qKXW4P9wSpab5H7LrLtOOPUUcvQk=
    - identity: {}
```

### Change secret key
Secret key can be generated using the following command:
```
head -c 32 /dev/urandom | base64
```
In encrypt_config.yaml,  replace secret for key1 in aescbc.keys section


### Change rights on directory and file
As the encryption key is also the key that will uncrypt Etcd, we will try to protect it as much as possible by changing rights on directory and file:
```
sudo chmod -R 600 /etc/kubernetes/aescbc
```

## Configure Kubernetes Api Server
Encryption will be done at Kubernetes Api Server level.
We will now configure this server to crypt secrets


### configure kube-apiserver.yaml
Edit ```kube-apiserver.yaml``` configuration file:
```
vim /etc/kubernetes/manifests/kube-apiserver.yaml
```

In spec.containers.command section add:
```
    - --encryption-provider-config=/etc/kubernetes/aescbc/encrypt_config.yaml
```

In spec.containers.volumeMounts section add:
```
    - mountPath: /etc/kubernetes/aescbc
      name: aescbc-config
      readOnly: true
```

In spec.volumes section add:
```
  - hostPath:
      path: /etc/kubernetes/aescbc
      type: DirectoryOrCreate
    name: aescbc-config
```
save the file

### verify api server
When saving file, Kubernetes will detect changes and restart Api Server.
This can be verified using the following command:
```
kubectl -n kube-system get pods
```
```
NAME                             READY   STATUS    RESTARTS   AGE
coredns-66bff467f8-69b8r         1/1     Running   0          21h
coredns-66bff467f8-74j9n         1/1     Running   0          21h
etcd-cube05                      1/1     Running   0          21h
kube-apiserver-cube05            1/1     Running   0          6s
kube-controller-manager-cube05   1/1     Running   1          21h
kube-flannel-ds-amd64-p9xhq      1/1     Running   0          20h
kube-proxy-8xk5g                 1/1     Running   0          21h
kube-scheduler-cube05            1/1     Running   1          21h
``` 
At this state, all created secrets will be crypted in etcd

## Verify secrets encryption

### Create a secret
```
kubectl create secret generic secret1 -n default --from-literal=mykey=mydata
```

### Verify secret creation
```
sudo kubectl -n default describe secret secret1
```
``` 
Name:         secret1
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
mykey:  6 bytes
```

### Verify secret encryption
To verify secret encryption we will install etcd client package
```
apt-get install etcd-client
```

Run the following command:
```
ETCDCTL_API=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/ca.crt --key=/etc/kubernetes/pki/etcd/ca.key \
--endpoints=https://localhost:2379 get /registry/secrets/default/secret1
```
Output will appear with the following text ```k8s:enc:aescbc:v1:key1:``` followed by binary values.

Secrets are now encoded with aescbc v1 provider using key1



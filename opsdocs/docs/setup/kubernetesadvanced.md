### Install Opendekstop on a cluster

For advanced installation, we will put abcdesktop on a kubernetes multi-master cluster. 

For this, we will need 6 VMs :  
 - 1 Master Control Plane  
 - 2 Control Plane  
 - 3 Workers  

All VMs require 2 CPU, 2Go Ram and 30Go HDD.
Meaning you will need 12 CPU, 12Go Ram and 180Go HDD

The following procedure has been executed on a Ubuntu 18.04 server.

#### Create VMs

To create and manage VMs, we will create scripts and files :  
- serverlist.sh - Servers Names and IP to manage  
- default.xml - Modified KVM default network definition to add domain name for DNS resolution inside cluster  
- create-vm.sh - Script to create pre-configured Ubuntu 18.04 VMs  
- do_all.sh - Script to create all VMs and network for all cluster servers  
- delete-vm.sh - Script to delete all created VMs  

All chapters actions will be done on host server.  
VMs creation can be skipped if you have your own cluster or you wan't to create it in a different way.

##### Install libvirt and kvm pacakges

```  
  sudo apt-get install -qy \
  qemu-kvm virtinst bridge-utils cpu-checker libvirt-clients libvirt-daemon-system 
```

#### Create VM creation files

##### serverlist.sh file

serverlist.sh file will let you define server names and IP using a bash dictionnary.

Create ``` serverlist.sh ``` file copying the following lines:
```
unset newipdict
declare -A newipdict
newipdict["k8s-master"]="192.168.122.11"
newipdict["k8s-cp1"]="192.168.122.12"
newipdict["k8s-cp2"]="192.168.122.13"
newipdict["k8s-ws1"]="192.168.122.14"
newipdict["k8s-ws2"]="192.168.122.15"
newipdict["k8s-ws3"]="192.168.122.16"
```


##### default.xml file

default.xml file is a modified version of default network created by libvirt/KVM.
This file just add domain name to let server names DNS resolution working.

Create ```default.xml``` file copying the following lines:
```
<network>
  <name>default</name>
  <uuid>067c864a-2704-4dbb-b997-2b3006640623</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:a6:b9:2f'/>
  <domain name='abcdesktop.local' localOnly='yes'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>
```

##### create-vm.sh file
This file is the template to create cluster VMs.
VMs will be configured for french. You will have to modify Ubuntu Preseed for your country. (This is the hard part of the procedure)

Create ```create-vm.sh``` file copying the following lines:
```
#!/bin/bash

if [ -z "$1" ] ;
then
 echo Specify a virtual-machine name.
 exit 1
fi

NAME=$1
NTPSERVER="fr.pool.ntp.org"
USERNAME="abcdesktop"
PASSWORD="password"

function cleanup_preseed_cfg() {
    rm -v -f $PRESEED_FILE
    rmdir -v $PRESEED_DIR
}

function generate_preseed_cfg() {
    PRESEED_DIR=/tmp/preseed$$
    PRESEED_BASENAME=preseed.cfg
    PRESEED_FILE=$PRESEED_DIR/$PRESEED_BASENAME
    mkdir -p $PRESEED_DIR
    cat > $PRESEED_FILE <<EOF
d-i debian-installer/language string C
d-i debian-installer/locale string fr_FR.UTF-8
d-i debian-installer/country string FR
d-i keymap select fr(latin9)
d-i keyboard-configuration/toggle select No toggling
d-i keyboard-configuration/layout string French
d-i     keyboard-configuration/variant  string
d-i console-setup/ask_detect boolean false
d-i console-setup/layoutcode string fr
d-i netcfg/choose_interface select auto
d-i netcfg/get_hostname string $NAME
d-i netcfg/get_domain string localdomain
d-i netcfg/wireless_wep string
d-i mirror/country string FR
d-i mirror/http/hostname string archive.ubuntu.com
d-i mirror/http/directory string /ubuntu
d-i mirror/http/proxy string $PROXY
d-i mirror/http/mirror select archive.ubuntu.com
d-i clock-setup/utc boolean true
d-i time/zone string Europ/Paris
d-i clock-setup/ntp boolean true
d-i clock-setup/ntp-server string $NTPSERVER
d-i partman-auto/method string lvm
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-lvm/confirm boolean true
d-i partman-lvm/confirm_nooverwrite boolean true
d-i partman-auto-lvm/guided_size string max
# - atomic: all files in one partition
# - home:   separate /home partition
# - multi:  separate /home, /usr, /var, and /tmp partitions
d-i partman-auto/choose_recipe select atomic
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select Finish partitioning and write changes to disk
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
d-i passwd/user-fullname string $USERNAME
d-i passwd/username string $USERNAME
d-i passwd/user-password password $PASSWORD
d-i passwd/user-password-again password $PASSWORD
d-i user-setup/allow-password-weak boolean true
d-i user-setup/encrypt-home boolean false
#tasksel tasksel/first multiselect
tasksel tasksel/first multiselect standard
d-i apt-setup/restricted boolean true
d-i apt-setup/universe boolean true
d-i apt-setup/backports boolean true
d-i apt-setup/local0/repository string deb https://apt.kubernetes.io/ kubernetes-xenial main
d-i apt-setup/local0/comment string Kubernetes Packages
d-i apt-setup/local0/source boolean false
d-i apt-setup/local0/key string http://packages.cloud.google.com/apt/doc/apt-key.gpg
d-i pkgsel/include string openssh-server build-essential acpid git-core ntp \
                          docker.io containerd gnupg openssl iptables acl \
                          python3-openssl apt-transport-https kubectl=1.17.0-00 kubelet=1.17.0-00 kubeadm=1.17.0-00
d-i pkgsel/upgrade select none
d-i pkgsel/update-policy select none
d-i grub-installer/only_debian boolean true
d-i grub-installer/with_other_os boolean true
d-i finish-install/reboot_in_progress note
d-i preseed/late_command string \
    sed -i "s;quiet;quiet console=ttyS0;" /target/etc/default/grub ;   \
    sed -i "s;quiet;quiet console=ttyS0;g" /target/boot/grub/grub.cfg ; \
    echo '$USERNAME ALL=(ALL) NOPASSWD: ALL' >/target/etc/sudoers.d/$USERNAME ; \
    in-target chmod 440 /etc/sudoers.d/$USERNAME ; \
    in-target swapoff -a ; \
    in-target rm -f /swapfile ; \
    in-target usermod -aG docker $USERNAME ; \
    in-target sed -ri '/\sswap\s/s/^#?/#/' /etc/fstab ; \
    in-target sed -i "/ExecStart/s/$/ -H tcp:\/\/0.0.0.0:2376/g" /lib/systemd/system/docker.service ; \
    in-target systemctl enable docker.service ; \ 
    in-target mkdir /mnt/oio ; \
    in-target rm -f /etc/udev/rules.d/70-persistent-net.rules
EOF
}

generate_preseed_cfg

sudo virt-install \
--name $1 \
--ram 2096 \
--check all=off \
--disk path=/var/lib/libvirt/images/$1.qcow2,size=30,bus=virtio \
--vcpus 2 \
--os-type linux \
--os-variant ubuntu18.04 \
--network bridge=virbr0 \
--graphics none \
--console pty,target_type=serial \
--initrd-inject $PRESEED_FILE \
--location 'http://gb.archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/' \
--extra-args 'console=ttyS0,115200n8 serial'

cleanup_preseed_cfg

```

Change rights to make file executable:
```
chmod 777 create-vm.sh
```

##### do_all.sh file

This script will check VMs to create and if not available, will call VM template creation script and add necessary network entries.

Create ```do_all.sh``` file copying the following lines:

```
#!/bin/bash

source serverlist.sh

guesttowait=()

# check if guest already exists
vms=$(virsh list --all|tail -n +3|head -n -1|awk '{ print $2 }')
for vm in ${!newipdict[@]}
do
    if [[ $vms =~ "${vm}" ]]
    then
        echo "${vm} already exists ! We won't run guest creation for this value"
    else
	echo "Creating guest ${vm} this may take several minutes"
	guesttowait+=("${vm}")
	./create-vm.sh ${vm} &
    fi;
done

nbtowait=${#guesttowait[@]}
if [ "$nbtowait" -eq 0 ]
then 
    echo "All guests already created, nothing to do..."
    exit 0
fi

sleep 1

echo "Adding domain name for cluster name resolving"
virsh net-undefine default
virsh net-define default.xml
virsh start default
virsh net-autostart default

concserv=$( IFS=$'|'; echo "${guesttowait[*]}" )
nb=$(virsh list --all | grep -E ${concserv} | grep "shut off"|wc -l)

while [ "$nb" -ne "$nbtowait" ]
do
   echo "still waiting for ${guesttowait[*]} to create and shut off"
   sleep 10
   # concserv=$( IFS=$'|'; echo "${guesttowait[*]}" )
   nb=$(virsh list --all | grep -E ${concserv} | grep "shut off"|wc -l)
   virsh list --all | grep -E concserv
done

for name in ${guesttowait[*]}
do
    echo "Fixing IP for $name"
    mac=$(virsh domiflist ${name}|head -n +3|tail -n +3|awk '{print $5}')
    newip=${newipdict[$name]};

    todelete=$(virsh net-dumpxml default | grep "${name}"| grep -o "<[^>]*>")
    if [[ ! -z $todelete ]]
    then
        echo "deleting : ${todelete}"
        virsh net-update default delete ip-dhcp-host "${todelete}" --live --config
    fi
    echo "creating : <host mac='${mac}' name='${name}' ip='${newip}'/>"
    virsh net-update default add ip-dhcp-host "<host mac='${mac}' name='${name}' ip='${newip}'/>" --live --config

    echo "restarting link"
    virsh domif-setlink ${name} ${mac} down
    virsh domif-setlink ${name} ${mac} up

done

virsh net-dumpxml default
```

Change rights to make file executable:
```
chmod 777 do_all.sh
```

##### delete-vm.sh file

This script will read server list and delete all matching VM names.

Create ```delete-vm.sh``` file copying the following lines:

```
#!/bin/bash

source serverlist.sh

vms=$(virsh list --all|tail -n +3|head -n -1|awk '{ print $2 }')
for vm in ${!newipdict[@]}
do
    if [[ $vms =~ "${vm}" ]]
    then
        echo "Deleting ${vm}"
        sudo virsh shutdown ${vm}
        sudo virsh destroy ${vm}
        sudo virsh undefine ${vm} --remove-all-storage
        echo "${vm} deleted"
    else
	echo "VM ${vm} not found. We do nothing"
    fi;
done

virsh list --all
```

Change rights to make file executable:
```
chmod 777 delete-vm.sh
```

#### Run cluster creation

Cluster creation will create the 6 necessary VMs. The process will be long (about 1 hour, depending off your network connection) as we will download a Ubuntu 18.04 and all necessary packages for kubernetes and abcdesktop.

Run the following command and go for a coffee :
``` 
do_all.sh
```

During VMs creation, you will see the following message every 10 seconds :
``` 
still waiting for k8s-master  k8s-cp1  k8s-cp2 k8s-ws1 k8s-ws2 k8s-ws3 to create and shut off
```
Script will wait for all servers to be created and shut down before creating network connections

Once everything has been done, you should see the following state for all VMs :
```  
sudo virsh list --all
```
```
 Id   Name         State
-----------------------------
 -    k8s-cp1      shut off
 -    k8s-cp2      shut off
 -    k8s-master   shut off
 -    k8s-ws1      shut off
 -    k8s-ws2      shut off
 -    k8s-ws3      shut off

```

All servers can now be started manually with the following commands or using virt-manager GUI :
```
virsh start k8s-master
virsh start k8s-cp1
virsh start k8s-cp2
virsh start k8s-vm1
virsh start k8s-vm2
virsh start k8s-vm3
```

#### Kubernetes cluster creation

At this state, you are ready to create kubernetes cluster.
We will create HAproxy configuration and init master controle plane, additionnal control planes and workers.

##### HAproxy server

HAproxy will be the entrypoint for kubernetes control planes and abcdesktop access.

Connect k8s-master using ssh (default password is ```password```):
``` 
ssh abcdesktop@192.168.122.11
```

Install haproxy package:
```
sudo apt install haproxy
```

Modify haproxy configuration:
```
sudo vi /etc/haproxy/haproxy.cfg
``` 

```
global
	log /dev/log	local0
	log /dev/log	local1 notice
	chroot /var/lib/haproxy
	stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
	stats timeout 30s
	user haproxy
	group haproxy
	daemon

	# Default SSL material locations
	ca-base /etc/ssl/certs
	crt-base /etc/ssl/private

	# Default ciphers to use on SSL-enabled listening sockets.
	# For more information, see ciphers(1SSL). This list is from:
	#  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
	# An alternative list with additional directives can be obtained from
	#  https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=haproxy
	ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
	ssl-default-bind-options no-sslv3

defaults
	log	global
	mode	tcp
	option	tcplog
	option	dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
	errorfile 400 /etc/haproxy/errors/400.http
	errorfile 403 /etc/haproxy/errors/403.http
	errorfile 408 /etc/haproxy/errors/408.http
	errorfile 500 /etc/haproxy/errors/500.http
	errorfile 502 /etc/haproxy/errors/502.http
	errorfile 503 /etc/haproxy/errors/503.http
	errorfile 504 /etc/haproxy/errors/504.http

frontend api-front
    bind 192.168.122.11:8443
    bind 127.0.0.1:8443
    mode tcp
    option tcplog
    use_backend api-backend

backend api-backend
    mode tcp
    option tcplog
    option tcp-check
    balance roundrobin
    # balance source
    server master1  192.168.122.11:6443 check
    server master2  192.168.122.12:6443 check
    server master3  192.168.122.13:6443 check

frontend api-front2
    bind 192.168.122.11:1234
    bind 127.0.0.1:1234
    mode tcp
    option tcplog
    use_backend api-backend2

backend api-backend2
    mode tcp
    option tcplog
    option tcp-check

    # option httpcheck
    balance roundrobin
    # balance source
    default-server inter 3s fall 3 rise 2
    server ws1  192.168.122.14:30443 check
    server ws2  192.168.122.15:30443 check
    server ws3  192.168.122.16:30443 check
```

Control planes will communicate over 192.168.122.11:8443 entrypoint
abcdesktop will be available connecting 192.168.122.11:1234 address

Restart haproxy service to apply configuration
```
sudo systemctl restart haproxy.service
```
Enable haproxy service:
```
sudo systemctl enable haproxy.service
```


##### Init master controle plane

Create kubeadm config file :
```
vi ./kubeadm-config.yaml
```
```
apiVersion: kubeadm.k8s.io/v1beta1
kind: ClusterConfiguration
kubernetesVersion: stable
apiServer:
  certSANs:
  - "192.168.122.11"
controlPlaneEndpoint: "192.168.122.11:8443"
networking:
   podSubnet: "10.244.0.0/16"
```

Launch kubeadm init configuration
```
sudo kubeadm init --config=kubeadm-config.yaml --upload-certs
```

Last messages of the command are the important parts, copy them in a file :
```
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of the control-plane node running the following command on each as root:

  kubeadm join 192.168.122.11:8443 --token b6e1s0.e1h4r8h6byavke8z \
    --discovery-token-ca-cert-hash sha256:54b72a18e02641f5b38bb48b436814530333b0ab16f6c1d72408abb547a49ca9 \
    --control-plane --certificate-key a71a13880fd492e32436df72d5a872f05205748a697f6c63f0d2a9d6c66eaf76

Please note that the certificate-key gives access to cluster sensitive data, keep it secret!
As a safeguard, uploaded-certs will be deleted in two hours; If necessary, you can use
"kubeadm init phase upload-certs --upload-certs" to reload certs afterward.

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.122.11:8443 --token b6e1s0.e1h4r8h6byavke8z \
    --discovery-token-ca-cert-hash sha256:54b72a18e02641f5b38bb48b436814530333b0ab16f6c1d72408abb547a49ca9 

```

First execute the following part of the message :
```
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Now connect using ssh to all cotrol planes (k8s-cp1 and k8s-cp2) and execute the following command to let additionnal control planes to join cluster (Copy/Past command from master init messages) :
```
sudo  kubeadm join 192.168.122.11:8443 --token b6e1s0.e1h4r8h6byavke8z \
    --discovery-token-ca-cert-hash sha256:54b72a18e02641f5b38bb48b436814530333b0ab16f6c1d72408abb547a49ca9 \
    --control-plane --certificate-key a71a13880fd492e32436df72d5a872f05205748a697f6c63f0d2a9d6c66eaf76
```

Now connect using ssh to all workers (k8s-ws1, k8s-ws2 and k8s-ws3) and execute the following command (Copy/Past command from master init messages):
```
sudo kubeadm join 192.168.122.11:8443 --token b6e1s0.e1h4r8h6byavke8z \
    --discovery-token-ca-cert-hash sha256:54b72a18e02641f5b38bb48b436814530333b0ab16f6c1d72408abb547a49ca9 
```

At this state, all nodes should be to "NotReady" state.
```
abcdesktop@k8s-master:~$ kubectl get nodes
NAME         STATUS     ROLES    AGE    VERSION
k8s-cp1      NotReady      master   56m    v1.17.0
k8s-cp2      NotReady      master   58m    v1.17.0
k8s-master   NotReady      master   59m    v1.17.0
k8s-ws1      NotReady      <none>   7m2s   v1.17.0
k8s-ws2      NotReady      <none>   89s    v1.17.0
k8s-ws3      NotReady   <none>   39s    v1.17.0
```

Kubernetes need cni definition to become "Ready". We will use flannel for this:
```
kubectl apply -f https://github.com/coreos/flannel/raw/master/Documentation/kube-flannel.yml
```

Now, all nodes should be "Ready"
```
abcdesktop@k8s-master:~$ kubectl get nodes
NAME         STATUS     ROLES    AGE    VERSION
k8s-cp1      Ready      master   56m    v1.17.0
k8s-cp2      Ready      master   58m    v1.17.0
k8s-master   Ready      master   59m    v1.17.0
k8s-ws1      Ready      <none>   7m2s   v1.17.0
k8s-ws2      Ready      <none>   89s    v1.17.0
k8s-ws3      Ready   <none>   39s    v1.17.0
```

##### Install abcdesktop

First we create opendeksotp namespace:
```
sudo kubectl create namespace abcdesktop
```

Change default namespace to abcdesktop:
```
kubectl config set-context $(kubectl config current-context) --namespace=abcdesktop
```

Create abcdesktop secrets:
```
# build rsa kay pairs for jwt payload 
# 256 bits is a small value, change here if need
# rm abcdesktop_jwt_desktop_payload_private_key.pem _abcdesktop_jwt_desktop_payload_public_key.pem abcdesktop_jwt_desktop_payload_public_key.pem
# rm abcdesktop_jwt_desktop_signing_private_key.pem abcdesktop_jwt_desktop_signing_public_key.pem

openssl genrsa  -out abcdesktop_jwt_desktop_payload_private_key.pem 512
openssl rsa     -in  abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem
openssl rsa -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem

# build rsa kay pairs for jwt signing 
openssl genrsa -out abcdesktop_jwt_desktop_signing_private_key.pem 1024
openssl rsa     -in abcdesktop_jwt_desktop_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_desktop_signing_public_key.pem

# kubectl delete secrets abcdesktopjwtdesktoppayload abcdesktopjwtdesktopsigning -n abcdesktop
kubectl create secret generic abcdesktopjwtdesktoppayload --from-file=abcdesktop_jwt_desktop_payload_private_key.pem --from-file=abcdesktop_jwt_desktop_payload_public_key.pem --namespace=abcdesktop
kubectl create secret generic abcdesktopjwtdesktopsigning --from-file=abcdesktop_jwt_desktop_signing_private_key.pem --from-file=abcdesktop_jwt_desktop_signing_public_key.pem --namespace=abcdesktop
```


At this step it is recommended to pull necessary docker images on each workers.
Kubernetes will attemp to pull them, but you will have no monitoring of pull advance.
As abcdesktop images are quite heavy, this would result in various errors when trying to access abcdesktop before the end. Minimal image list can be found at top of this link : [kubernetes](../kubernetesmode) 

abcdesktop deployment will be done with the following command :
```
kubectl create -f http://docs.abcdesktop.io/setup/abcdesktop.yaml
```
```
abcdesktop@k8s-master:~$ kubectl create -f http://docs.abcdesktop.io/setup/abcdesktop.yaml
clusterrole.rbac.authorization.k8s.io/pyos-role created
clusterrolebinding.rbac.authorization.k8s.io/pyos-rbac created
serviceaccount/pyos-serviceaccount created
storageclass.storage.k8s.io/storage-local-abcdesktop created
persistentvolume/pv-volume-home-directory created
persistentvolumeclaim/persistentvolumeclaim-home-directory created
configmap/abcdesktop-config created
configmap/nginx-config created
deployment.apps/memcached-od created
deployment.apps/mongodb-od created
daemonset.apps/daemonset-nginx created
deployment.apps/speedtest-od created
daemonset.apps/daemonset-pyos created
service/memcached created
service/mongodb created
service/speedtest created
service/nginx created
service/pyos created
```
abcdesktop.yaml can be downloaded manually here :
<a href="/setup/abcdesktop.yaml" download>abcdesktop.yaml</a>



abcdesktop deployment can be verified with the following command :
```
abcdesktop@k8s-master:~$ kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
daemonset-nginx-4ql2g           1/1     Running   0          34m
daemonset-nginx-7zxdc           1/1     Running   0          34m
daemonset-nginx-s8wmk           1/1     Running   0          34m
daemonset-pyos-97qmt            1/1     Running   0          34m
daemonset-pyos-k496h            1/1     Running   0          34m
daemonset-pyos-wngpg            1/1     Running   0          34m
memcached-od-db69c45fb-hbzld    1/1     Running   0          34m
mongodb-od-86bbf5c655-xjldj     1/1     Running   0          34m
speedtest-od-6567f8b4c4-tfqsl   1/1     Running   0          34m

```
If everything is at "Running" status, you can then start testing


#### Test abcdesktop

Simply connect to the following address with your web browser :
```
http://192.168.122.11:1234
``` 

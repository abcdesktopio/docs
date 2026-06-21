---
title: Network Policy Architecture for abcdesktop.io | abcdesktop.io
description: Detailed specification of the Kubernetes NetworkPolicy rules used by abcdesktop.io, including allowed TCP ports and inter-pod communication rules.
keywords: NetworkPolicy, network policy, TCP ports, inter-pod, Calico, Cilium, Kubernetes, security, abcdesktop
tags:
  - netpol
  - network
  - policy
  - overview
  - AD
  - security
  - NetworkPolicy
  - architecture
---

# Netpol

## Goals

* Apply network policies to control traffic flow at the IP address or port level for all abcdesktop pods, **including user pods**.


## Authors


[jpxavier-oio](https://github.com/jpxavier-oio) designed the network policy architecture for abcdesktop.io.



## Requirements

- A Kubernetes cluster is required, and the `kubectl` command-line tool must be configured to communicate with your cluster. It is recommended to run this tutorial on a cluster with at least two nodes.

- Network policies are implemented by the network plugin. To use network policies, you must use a networking solution that supports `NetworkPolicy`.



## NetworkPolicy description


abcdesktop defines two types of isolation policies: the NetworkPolicy `rights` and the NetworkPolicy `permits`.


- The NetworkPolicy `rights` contains `egress` and `ingress` rules for pods selected by label. The `rights` policy controls both inbound access to a pod (ingress) and outbound access from a pod (egress). To define IP filters for user pods, configure egress NetworkPolicy rules within the `rights` policy.


- The NetworkPolicy `permits` contains `egress` rules targeting a pod selected by label. The NetworkPolicy `permits` grants outbound connectivity to the specified target pod.


## NetworkPolicy example

The NetworkPolicy examples below describe the network policies applied to the internal memcached pod and to user pods.

### NetworkPolicy `rights` and `permits` for the `memcached` service

The `memcached` service listens on TCP port 11211.

The NetworkPolicy for the memcached service `rights`:
- is named `memcached-rights`,
- selects pods with the label `run: memcached-od`,
- and permits inbound traffic on TCP port 11211.


```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: memcached-rights
  namespace: abcdesktop
spec:
  podSelector:
    matchLabels:
      run: memcached-od
  policyTypes:
  - Ingress
  ingress:
  - ports:
    - protocol: TCP
      port: 11211
    from:
    - podSelector:
        matchLabels:
          netpol/memcached: 'true'
    - namespaceSelector:
        matchLabels:
          name: kube-monitor
      podSelector:
        matchLabels:
          netpol/metrics: 'true'
```


The NetworkPolicy for the memcached service `permits`, named `memcached-permits`, allows all pods with the label `netpol/memcached: 'true'` to establish outbound connections to TCP port 11211 on pods with the label `run: memcached-od`.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: memcached-permits
  namespace: abcdesktop
spec:
  podSelector:
    matchLabels:
      netpol/memcached: 'true'
  policyTypes:
  - Egress
  egress:
  - ports:
    - protocol: TCP
      port: 11211
    to:
    - podSelector:
        matchLabels:
          run: memcached-od
---
```


### NetworkPolicy `rights` and `permits` for user pods


The `ocuser` pod listens on the following TCP ports:

  - 4714
  - 6081
  - 29780
  - 29781
  - 29782
  - 29783
  - 29784
  - 29785
  - 29786

The network policy for `ocuser` pods `rights` is named `ocuser-rights`. It selects pods with the label `type: 'x11server'` and permits inbound traffic on the ports listed above.

The `egress` network policy permits the following outbound traffic:

- DNS queries to kube-dns
- HTTP to any web site
- HTTPS to any web site
- Kerberos authentication to any KDC


```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ocuser-rights
  namespace: abcdesktop
spec:
  podSelector:
    matchLabels:
      type: 'x11server'
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          netpol/ocuser: 'true'
    ports:
    - protocol: TCP
      port: 4714
    - protocol: TCP
      port: 6081
    - protocol: TCP
      port: 8000
    - protocol: TCP
      port: 29780
    - protocol: TCP
      port: 29781
    - protocol: TCP
      port: 29782
    - protocol: TCP
      port: 29783
    - protocol: TCP
      port: 29784
    - protocol: TCP
      port: 29785
    # spawner_service_tcp_port
    - protocol: TCP
      port: 29786
  egress:
  # pod user can run dns query to all kube-system
  - ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
    to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
# permit www website from pod user 
  - ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 80
# permit kerberos auth kinit
  - ports:
    - protocol: UDP
      port: 88
    - protocol: TCP
      port: 88
```      


The network policy for `ocuser` pods `permits` is named `ocuser-permits`. It allows pods with the label `netpol/ocuser: 'true'` to establish outbound connections to the user pod services.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ocuser-permits
  namespace: abcdesktop
spec:
  podSelector:
    matchLabels:
      netpol/ocuser: 'true'
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          type: 'x11server'
    ports:
    # default pulseaudio websocket audio without webrtc gateway
    - protocol: TCP
      port: 4714
    # vnc websockify
    - protocol: TCP
      port: 6081
    # reserved
    - protocol: TCP
      port: 29780
    # xterm_tcp_port
    - protocol: TCP
      port: 29781
    # printerfile_service_tcp_port
    - protocol: TCP
      port: 29782
    # file_service_tcp_port
    - protocol: TCP
      port: 29783
    # broadcast_tcp_port 
    - protocol: TCP
      port: 29784
    # reserved
    - protocol: TCP
      port: 29785
    # spawner_service_tcp_port
    - protocol: TCP
      port: 29786
```

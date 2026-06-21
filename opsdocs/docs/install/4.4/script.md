---
title: Quick Install abcdesktop.io Using a Script | abcdesktop.io
description: Quick-start guide to deploying abcdesktop.io core services on Kubernetes using the one-line install script on Linux, macOS, and Windows.
keywords: install, script, quick start, Kubernetes, abcdesktop, Linux, macOS, Windows, one-line
tags:
  - bash
  - installation
  - setup
  - quick start
  - script
---

# Quick Installation Using the Bash Script

> A Linux operating system is recommended for running abcdesktop.io.

=== "Linux or macOS"

    ## Prerequisites

    - A Kubernetes cluster in the `Ready` state
    - The `kubectl` command-line tool configured to communicate with your cluster
    - `openssl` and `curl` installed on the local machine (required only for the `kubectl`-based installation method)

    ## Running the Installation Script

    Download and execute the latest release installation script:

    ```bash
    curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-{{ abcdesktop.latest_release }}.sh |bash
    ```

    > The following video demonstrates how to install abcdesktop.io on a freshly provisioned Kubernetes cluster using the bash script.

    <div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/vjapgK1ILTw" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>

    Expected stdout output:

    ??? note "show details"
        ```
        [INFO] abcdesktop install script namespace=abcdesktop
        [OK] kubectl version
        [OK] openssl version
        [OK] kubectl create namespace abcdesktop
        writing RSA key
        writing RSA key
        [OK] abcdesktop_jwt_desktop_payload keys created
        writing RSA key
        [OK] abcdesktop_jwt_desktop_signing keys create
        writing RSA key
        [OK] abcdesktop_jwt_user_signing keys create
        [OK] create secret generic abcdesktopjwtdesktoppayload
        [OK] create secret generic abcdesktopjwtdesktopsigning
        [OK] create secret generic abcdesktopjwtusersigning
        [OK] label secret abcdesktopjwtdesktoppayload
        [OK] label secret abcdesktopjwtdesktopsigning
        [OK] label secret abcdesktopjwtusersigning
        [OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-{{ abcdesktop.latest_release }}.yaml
        [OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.{{ abcdesktop.latest_release }}
        [OK] kubectl create configmap abcdesktop-config --from-file=od.config -n abcdesktop
        [OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
        role.rbac.authorization.k8s.io/pyos-role created
        rolebinding.rbac.authorization.k8s.io/pyos-rbac created
        serviceaccount/pyos-serviceaccount created
        configmap/configmap-mongodb-scripts created
        secret/secret-mongodb created
        deployment.apps/mongodb-od created
        deployment.apps/memcached-od created
        deployment.apps/router-od created
        deployment.apps/nginx-od created
        deployment.apps/speedtest-od created
        deployment.apps/pyos-od created
        deployment.apps/console-od created
        deployment.apps/openldap-od created
        endpoints/desktop created
        service/desktop created
        service/memcached created
        service/mongodb created
        service/speedtest created
        service/pyos created
        service/console created
        service/http-router created
        service/website created
        service/openldap created
        [INFO] waiting for deployment/console-od available
        [OK] deployment.apps/console-od condition met
        [INFO] waiting for deployment/memcached-od available
        [OK] deployment.apps/memcached-od condition met
        [INFO] waiting for deployment/mongodb-od available
        [OK] deployment.apps/mongodb-od condition met
        [INFO] waiting for deployment/nginx-od available
        [OK] deployment.apps/nginx-od condition met
        [INFO] waiting for deployment/openldap-od available
        [OK] deployment.apps/openldap-od condition met
        [INFO] waiting for deployment/pyos-od available
        [OK] deployment.apps/pyos-od condition met
        [INFO] waiting for deployment/router-od available
        [OK] deployment.apps/router-od condition met
        [INFO] waiting for deployment/speedtest-od available
        [OK] deployment.apps/speedtest-od condition met
        [INFO] list all pods in namespace abcdesktop
        NAME                            READY   STATUS    RESTARTS   AGE
        console-od-844c749f85-vbbb7     1/1     Running   0          32s
        memcached-od-d4b6b6867-tbfgf    1/1     Running   0          33s
        mongodb-od-5d996fd57b-tcn45     1/1     Running   0          33s
        nginx-od-796c7d7d6b-lgnjb       1/1     Running   0          33s
        openldap-od-567dcf7bf6-h2nq9    1/1     Running   0          32s
        pyos-od-8d4988b56-vcd7z         1/1     Running   0          32s
        router-od-f5458658-b52hj        1/1     Running   0          33s
        speedtest-od-7fcc9649b4-qllr7   1/1     Running   0          32s
        [INFO] Setup done
        [INFO] Checking the service url on http://localhost:30443
        [INFO] service status is down
        [INFO] Looking for a free TCP port from 30443
        [OK] Get a free TCP port from 30443
        [INFO] If you're using a cloud provider
        [INFO] Forwarding abcdesktop service for you on port=30443
        [INFO] For you setup is running the command 'kubectl port-forward nginx-od-796c7d7d6b-lgnjb --address 0.0.0.0 30443:80 -n abcdesktop'
        [OK] Port-Forward successful
        [OK] Please open your web browser and connect to

        [INFO] http://localhost:30443/

        ```

    The installation script performs the following steps in order:

    1. Creates the `abcdesktop` Kubernetes namespace.
    2. Generates RSA key pairs for JWT signing and payload encryption using `openssl`.
    3. Creates all required Kubernetes resources — ServiceAccount, RBAC roles, Services, Deployments, Secrets, and ConfigMaps — from the [abcdesktop.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-{{ abcdesktop.latest_release }}.yaml) manifest.
    4. Downloads the default configuration file [od.config](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/reference/od.config.{{ abcdesktop.latest_release }}) and creates the `abcdesktop-config` ConfigMap.

    > **Note:** This installation does not include application images. The desktop launches with only the minimal default applications available in the dock.

    Once the script completes, open a web browser and navigate to `http://localhost:30443/`.

    ## Changing the Default Namespace

    To deploy abcdesktop.io into a namespace other than the default `abcdesktop`, download the script and pass the `--namespace` option:

    ```bash
    wget https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-{{ abcdesktop.latest_release }}.sh
    chmod 755 install-{{ abcdesktop.latest_release }}.sh
    ```

    Run the script with a custom namespace:

    ```bash
    ./install-{{ abcdesktop.latest_release }}.sh --namespace superdesktop
    ```

    ??? note "show details"
        ```
        [INFO] abcdesktop install script namespace=superdesktop
        [OK] kubectl version
        [OK] openssl version
        [OK] kubectl create namespace superdesktop
        [OK] create secret generic abcdesktopjwtdesktoppayload
        [OK] create secret generic abcdesktopjwtdesktopsigning
        [OK] create secret generic abcdesktopjwtusersigning
        [OK] label secret abcdesktopjwtdesktoppayload
        [OK] label secret abcdesktopjwtdesktopsigning
        [OK] label secret abcdesktopjwtusersigning
        [OK] use local file abcdesktop.yaml
        [OK] use local file od.config
        [OK] updated abcdesktop.yaml file with new namespace superdesktop
        [OK] updated abcdesktop.yaml file with new fqdn superdesktop.svc.cluster.local
        [OK] updated od.config file with new namespace superdesktop
        [OK] updated od.config file with new fqdn superdesktop.svc.cluster.local
        [OK] kubectl create configmap abcdesktop-config --from-file=od.config -n superdesktop
        [OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
        [OK] default account is created
        [OK] role.rbac.authorization.k8s.io/pyos-role created
        rolebinding.rbac.authorization.k8s.io/pyos-rbac created
        serviceaccount/pyos-serviceaccount created
        configmap/configmap-mongodb-scripts created
        secret/secret-mongodb created
        deployment.apps/mongodb-od created
        deployment.apps/memcached-od created
        deployment.apps/router-od created
        deployment.apps/nginx-od created
        deployment.apps/speedtest-od created
        deployment.apps/pyos-od created
        deployment.apps/console-od created
        deployment.apps/openldap-od created
        endpoints/desktop created
        service/desktop created
        service/memcached created
        service/mongodb created
        service/speedtest created
        service/pyos created
        service/console created
        service/http-router created
        service/website created
        service/openldap created
        [OK] pyos-serviceaccount account is created
        [INFO] waiting for deployment/console-od available
        [OK] deployment.apps/console-od condition met
        [INFO] waiting for deployment/memcached-od available
        [OK] deployment.apps/memcached-od condition met
        [INFO] waiting for deployment/mongodb-od available
        [OK] deployment.apps/mongodb-od condition met
        [INFO] waiting for deployment/nginx-od available
        ```

=== "Windows"

    ## Prerequisites

    - A Kubernetes cluster in the `Ready` state
    - The `kubectl` command-line tool configured to communicate with your cluster
    - `openssl` and `curl` installed on the local machine

    ## Running the Installation Script

    Download and execute the latest release installation script:

    ```bash
    curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-{{ abcdesktop.latest_release }}.sh |bash
    ```

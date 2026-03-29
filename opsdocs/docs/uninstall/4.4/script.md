---
tags:
  - uninstall
  - bash
---
# Quick uninstall core services with a script

> Linux operating system is recommanded to run abcdesktop.io.

=== "Linux or macOS"

    ## Run the uninstall script

    Download and extract the uninstall bash script (Linux or macOS):

    ```bash
    curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.sh |bash
    ```

    You should read on stdout 

    ??? note "show details"
        ```bash
        abcdesktop uninstall script namespace=abcdesktop
        [OK] kubectl version
        [OK] kubectl get namespace abcdesktop
        [OK] delete pods --selector="type=x11server" -n abcdesktop
        [OK] use local file abcdesktop.yaml
        role.rbac.authorization.k8s.io "pyos-role" deleted
        rolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
        serviceaccount "pyos-serviceaccount" deleted
        configmap "configmap-mongodb-scripts" deleted
        secret "secret-mongodb" deleted
        deployment.apps "mongodb-od" deleted
        deployment.apps "memcached-od" deleted
        deployment.apps "router-od" deleted
        deployment.apps "nginx-od" deleted
        deployment.apps "speedtest-od" deleted
        deployment.apps "pyos-od" deleted
        deployment.apps "console-od" deleted
        deployment.apps "openldap-od" deleted
        endpoints "desktop" deleted
        service "desktop" deleted
        service "memcached" deleted
        service "mongodb" deleted
        service "speedtest" deleted
        service "pyos" deleted
        service "console" deleted
        service "http-router" deleted
        service "website" deleted
        service "openldap" deleted
        [OK] kubectl delete -f abcdesktop.yaml
        [OK] kubectl delete secrets --all -n abcdesktop
        [OK] kubectl delete configmap --all -n abcdesktop
        [OK] kubectl delete pvc --all -n abcdesktop
        [INFO] deleting namespace abcdesktop
        [OK] namespace "abcdesktop" deleted
        ```

    Please wait for the output message: 

    ```
    [OK] namespace "abcdesktop" deleted
    ```

    Great, you have uninstalled abcdesktop for kubernetes.

    ## Uninstall with a dedicated namespace


    ```bash
    wget https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.sh
    chmod 755 uninstall-4.4.sh
    ```

    Run the `uninstall-4.4.sh` command line with your own namespace

    ```
    ./uninstall-4.4.sh --namespace superdesktop
    ```

    You should read on stdout

    ??? note "show details"
        ```bash
        abcdesktop uninstall script namespace=superdesktop
        [OK] kubectl version
        [OK] kubectl get namespace superdesktop
        [OK] delete pods --selector="type=x11server" -n superdesktop
        [OK] use local file abcdesktop.yaml
        role.rbac.authorization.k8s.io "pyos-role" deleted
        rolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
        serviceaccount "pyos-serviceaccount" deleted
        configmap "configmap-mongodb-scripts" deleted
        secret "secret-mongodb" deleted
        deployment.apps "mongodb-od" deleted
        deployment.apps "memcached-od" deleted
        deployment.apps "router-od" deleted
        deployment.apps "nginx-od" deleted
        deployment.apps "speedtest-od" deleted
        deployment.apps "pyos-od" deleted
        deployment.apps "console-od" deleted
        deployment.apps "openldap-od" deleted
        endpoints "desktop" deleted
        service "desktop" deleted
        service "memcached" deleted
        service "mongodb" deleted
        service "speedtest" deleted
        service "pyos" deleted
        service "console" deleted
        service "http-router" deleted
        service "website" deleted
        service "openldap" deleted
        [OK] kubectl delete -f abcdesktop.yaml
        [OK] kubectl delete secrets --all -n superdesktop
        [OK] kubectl delete configmap --all -n superdesktop
        [OK] kubectl delete pvc --all -n superdesktop
        [INFO] deleting namespace superdesktop
        [OK] namespace "superdesktop" deleted
        ```

    Great, you have uninstalled abcdesktop for kubernetes with a dedicated namespace.


=== "Windows"

    ## Run the uninstall script

    Download and extract the uninstall PowerShell script (Windows):

    ```PowerShell
    $script = curl https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.ps1 

    Invoke-Expression $($script.Content)
    ```

    You should read on stdout 

    ??? note "show details"
        ```
        [INFO] abcdesktop uninstall script namespace=abcdesktop
        [OK] kubectl version
        [OK] kubectl get namespace abcdesktop
        [OK] delete pods --selector=\
        [OK] use local file abcdesktop.yaml
        role.rbac.authorization.k8s.io "pyos-role" deleted
        rolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
        serviceaccount "pyos-serviceaccount" deleted
        configmap "configmap-mongodb-scripts" deleted
        secret "secret-mongodb" deleted
        deployment.apps "mongodb-od" deleted
        deployment.apps "memcached-od" deleted
        deployment.apps "router-od" deleted
        deployment.apps "nginx-od" deleted
        deployment.apps "speedtest-od" deleted
        deployment.apps "pyos-od" deleted
        deployment.apps "console-od" deleted
        deployment.apps "openldap-od" deleted
        endpoints "desktop" deleted
        service "desktop" deleted
        service "memcached" deleted
        service "mongodb" deleted
        service "speedtest" deleted
        service "pyos" deleted
        service "console" deleted
        service "http-router" deleted
        service "website" deleted
        service "openldap" deleted
        [OK] kubectl delete -f abcdesktop.yaml
        [OK] kubectl delete secrets --all -n abcdesktop
        [OK] kubectl delete configmap --all -n abcdesktop
        [OK] kubectl delete pvc --all -n abcdesktop
        [INFO] deleting namespace abcdesktop
        [OK] namespace "abcdesktop" deleted
        [INFO] delete abcdesktop related files
        [OK] remove od.config abcdesktop.yaml poduser.yaml
        [OK] remove *.pem
        [INFO] abcdesktop was succesfully uninstalled
        ```

    ## Uninstall with a dedicated namespace


    ```PowerShell
    curl https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.ps1  -OutFile uninstall-4.4.ps1
    ```

    Run the `uninstall-4.4.ps1` command line with your own namespace

    ```PowerShell
    .\uninstall-4.4.ps1 --namespace superdesktop
    ```

    You should read on stdout

    ??? note "show details"
        ```
        [INFO] abcdesktop uninstall script namespace=superdesktop
        [OK] kubectl version
        [OK] kubectl get namespace superdesktop
        [OK] delete pods --selector=\
        [OK] use local file abcdesktop.yaml
        [OK] updated abcdesktop.yaml file with new namespace superdesktop
        role.rbac.authorization.k8s.io "pyos-role" deleted
        rolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
        serviceaccount "pyos-serviceaccount" deleted
        configmap "configmap-mongodb-scripts" deleted
        secret "secret-mongodb" deleted
        deployment.apps "mongodb-od" deleted
        deployment.apps "memcached-od" deleted
        deployment.apps "router-od" deleted
        deployment.apps "nginx-od" deleted
        deployment.apps "speedtest-od" deleted
        deployment.apps "pyos-od" deleted
        deployment.apps "console-od" deleted
        deployment.apps "openldap-od" deleted
        endpoints "desktop" deleted
        service "desktop" deleted
        service "memcached" deleted
        service "mongodb" deleted
        service "speedtest" deleted
        service "pyos" deleted
        service "console" deleted
        service "http-router" deleted
        service "website" deleted
        service "openldap" deleted
        [OK] kubectl delete -f abcdesktop.yaml
        [OK] kubectl delete secrets --all -n superdesktop
        [OK] kubectl delete configmap --all -n superdesktop
        [OK] kubectl delete pvc --all -n superdesktop
        [INFO] deleting namespace superdesktop
        [OK] namespace "superdesktop" deleted
        [INFO] delete abcdesktop related files
        [OK] remove od.config abcdesktop.yaml poduser.yaml
        [OK] remove *.pem
        [INFO] abcdesktop was succesfully uninstalled
        ```

---
tags:
  - uninstall
  - bash
---
# Uninstalling abcdesktop.io Core Services Using a Script

> A Linux operating system is recommended for running abcdesktop.io.

=== "Linux or macOS"

    ## Running the Uninstall Script

    Download and execute the uninstall script (Linux or macOS):

    ```bash
    curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.sh |bash
    ```

    The script produces the following standard output:

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

    Wait for the following confirmation message before proceeding:

    ```
    [OK] namespace "abcdesktop" deleted
    ```

    abcdesktop.io has been successfully removed from the Kubernetes cluster.

    ## Uninstalling with a Custom Namespace


    ```bash
    wget https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.sh
    chmod 755 uninstall-4.4.sh
    ```

    Run the `uninstall-4.4.sh` script with your custom namespace:

    ```
    ./uninstall-4.4.sh --namespace superdesktop
    ```

    The script produces the following standard output:

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

    abcdesktop.io has been successfully removed from the Kubernetes cluster using the custom namespace.


=== "Windows"

    ## Running the Uninstall Script

    Download and execute the uninstall PowerShell script (Windows):

    ```PowerShell
    $script = curl https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.ps1

    Invoke-Expression $($script.Content)
    ```

    The script produces the following standard output:

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

    ## Uninstalling with a Custom Namespace


    ```PowerShell
    curl https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.4.ps1  -OutFile uninstall-4.4.ps1
    ```

    Run the `uninstall-4.4.ps1` script with your custom namespace:

    ```PowerShell
    .\uninstall-4.4.ps1 --namespace superdesktop
    ```

    The script produces the following standard output:

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

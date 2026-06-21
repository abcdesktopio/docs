---
title: Install Applications Using a Script | abcdesktop.io
description: Guide to bulk-installing abcdesktop.io applications using the install script and a predefined application list for rapid deployment.
keywords: install applications, script, bulk install, application list, abcdesktop, Kubernetes
tags:
  - application
  - installation
  - bash
  - applications
  - script
---

# Installing Applications with the Default Script

=== "Linux or macOS"

    ## Quick Application Installation

    > The quick application installation script runs on Linux and macOS operating systems.

    Download and execute the `pullapps-{{ abcdesktop.latest_release }}.sh` script to install the default set of application images:

    ```bash
    curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/pullapps-{{ abcdesktop.latest_release }}.sh | bash
    ```

    The following video demonstrates the application installation process on a freshly provisioned Kubernetes cluster:

    <div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/JSIjnNA6kNE" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>


    ## Connecting to abcdesktop.io

    After the script completes, the `pyos` API server receives new image registration events. Refresh the browser tab to display the newly installed applications.

    Navigate to your abcdesktop.io instance:

    ```url
    http://localhost:30443/
    ```

    The installed applications are now available in the desktop environment.

    ![applications after upload json](img/abcdesktop-4-1-loginanonymous-with-applications.png)

    You can now launch installed applications. For example, launching Firefox demonstrates **Remote Browser Isolation (RBI)**: Firefox runs entirely inside an isolated container on the Kubernetes cluster, and only rendered pixels are streamed to the client browser.

    ![Start Firefox application](img/abcdesktop-4-1-loginanonymous-with-firefox-applications.png)

    The following video demonstrates application management using the admin console:

    <div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/Dah78eAJykw" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>

=== "Windows"

    ## Quick Application Installation

    > The quick application installation script runs on Windows operating systems.

    Download and execute the `pullapps-{{ abcdesktop.latest_release }}.ps1` PowerShell script:

    ```bash
    curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/pullapps-{{ abcdesktop.latest_release }}.ps1 | bash
    ```

    The following video demonstrates the application installation process on a freshly provisioned Kubernetes cluster:

    <div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/JSIjnNA6kNE" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>


    ## Connecting to abcdesktop.io

    After the script completes, refresh the browser tab to display the newly installed applications.

    Navigate to your abcdesktop.io instance:

    ```bash
    http://localhost:30443/
    ```

    The installed applications are now available in the desktop environment.

    ![applications after upload json](img/abcdesktop-4-1-loginanonymous-with-applications.png)

    You can now launch installed applications. For example, launching Firefox demonstrates **Remote Browser Isolation (RBI)**: Firefox runs entirely inside an isolated container on the Kubernetes cluster, and only rendered pixels are streamed to the client browser.

    ![Start Firefox application](img/abcdesktop-4-1-loginanonymous-with-firefox-applications.png)

    The following video demonstrates application management using the admin console:

    <div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/Dah78eAJykw" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>

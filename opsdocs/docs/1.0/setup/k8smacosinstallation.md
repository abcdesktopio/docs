
# MacOS/X Kubernetes

## Enable Kubernetes on MacOS/X 

Click on the Docker icon in MacOS/X menu bar.

![Docker in menu bar](img/kubernetes-macosx-docker-menubar.png)

Then choose ```Preferences...``` 

![Docker in menu bar preferences](img/kubernetes-macosx-docker-preference.png)


The following window should appear :

![Docker MacOS/X Preference](img/kubernetes-macosx-docker-general.png)

Choose ```Kubernetes```, then check the  ```Enable Kubernetes ``` 
![Kubernetes Docker MacOS/X Enable](img/kubernetes-macosx-docker-enable.png)


Kubernetes stay in ```Starting``` state during few minutes.
Please wait to download all container images and for kubernetes installation process.

![Kubernetes Docker MacOS/X Enable](img/kubernetes-macosx-docker-running.png)

On the bottom you should read next ```Docker Running``` ```Kubernetes Running```

![Kubernetes Docker MacOS/X Enable](img/kubernetes-macosx-docker-running-kubernetes-running.png)

Great, you have installed Kubernetes on MacOS/X.


## Run the new ```kubectl``` command

Open a Terminal, then run the command ```kubectl version``` 

``` 
% kubectl version
Client Version: version.Info{Major:"1", Minor:"15", GitVersion:"v1.15.5", GitCommit:"20c265fef0741dd71a66480e35bd69f18351daea", GitTreeState:"clean", BuildDate:"2019-10-15T19:16:51Z", GoVersion:"go1.12.10", Compiler:"gc", Platform:"darwin/amd64"}
Server Version: version.Info{Major:"1", Minor:"15", GitVersion:"v1.15.5", GitCommit:"20c265fef0741dd71a66480e35bd69f18351daea", GitTreeState:"clean", BuildDate:"2019-10-15T19:07:57Z", GoVersion:"go1.12.10", Compiler:"gc", Platform:"linux/amd64"}
``` 

Run the command ```kubectl get pods``` 

``` 
% kubectl get pods
No resources found.
``` 

Great, the kubectl command works. It's time to deploy abcdesktop.io
# Update and custom frontend web page


abcdesktop uses a front HTML web site and X11 Linux application. So, to get a new graphic design, you have to define it twice in HTML (CSS) files and in X11 config.

## Requirements 

* `docker` package installed 


## Goals

* Update abcdesktop default frontend web page to use your own.
* Create new image for abcdesktop oc.nginx

## Configure od.config to use the new color

In the od.config, add the env var `ABCDESKTOP_BG_COLOR`

```
desktop.envlocal :  {
  'X11LISTEN':'tcp', 
  'WEBSOCKIFY_HEARTBEAT':'30',
  'TURN_PROTOCOL': 'tcp',
  'ABCDESKTOP_BG_COLOR': ‘#18974c’ }
```

Then update the config map `abcdesktop-config` and restart deployment `pyos-od` 

```
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config -o yaml --dry-run=client | kubectl replace -n abcdesktop -f -
kubectl rollout restart deployment pyos-od -n abcdesktop
```

You should read on stdout

```
configmap/abcdesktop-config replaced
deployment.apps/pyos-od restarted
```

## Create new image for abcdesktop oc.nginx

### Clone default webmodules  

```bash
git clone -b 3.3 https://github.com/abcdesktopio/webModules.git
```

### Locate project and ui files 

#### Update ui.json file

Update your `ui.json` file.  `ui.json` is located in `transpile/config` directory.


```bash
# cd webModules/transpile/config
# ls -la
total 204
drwxrwxr-x   1 root root   4096 Feb  1 15:14 .
drwxr-xr-x   1 root root   4096 Feb  1 15:14 ..
-rw-rw-r--   1 root root     34 Feb  1 15:14 .cache.json
-rw-rw-r--   1 root root   2215 Feb  1 15:11 modules.json
-rw-rw-r--   1 root root   1044 Feb  1 15:11 ui.json
```

`ui.json` is a json dictionary file

The main entry is `name`, name is the project name:


| entry          | default value       | example          |
|----------------|---------------------|------------------|
| name           | abcdesktop.io       | acmedesktop.io   |


```json
{
  "name": "abcdesktop.io",
  "projectNameSplitedHTML": "<span id='projectNameSplitedStagea'>a</span><span id='projectNameSplitedStageb'>b</span><span id='projectNameSplitedStagec'>c</span><span id='p
rojectNameSplitedStaged'>desktop</span>",
  "colors": [
    {
      "name": "@x11bgcolor",
      "value": "#6EC6F0"
    },
    {
      "name": "@primary",
      "value": "#474B55"
    },
    {
      "name": "@secondary",
      "value": "#2D2D2D"
    },
    {
      "name": "@tertiary",
      "value": "#6EC6F0"
    },
    {
      "name": "@quaternary",
      "value": "#1E1E1E"
    },
    {
      "name": "@svgColor",
      "value": "#FFFFFF"
    },
    {
      "name": "@danger",
      "value": "#CD3C14"
    },
    {
      "name": "@success",
      "value": "#32C832"
    },
    {
      "name": "@info",
      "value": "#527EDB"
    },
    {
      "name": "@warning",
      "value": "#FFCC00"
    },
    {
      "name": "@light",
      "value": "#FFFFFF"
    },
    {
      "name": "@dark",
      "value": "#666666"
    },
    {
      "name": "@blue",
      "value": "#4BB4E6"
    },
    {
      "name": "@green",
      "value": "#50BE87"
    },
    {
      "name": "@purple",
      "value": "#A885D8"
    },
    {
      "name": "@pink",
      "value": "#FFB4E6"
    },
    {
      "name": "@yellow",
      "value": "#FFD200"
    }
  ],
  "urlcannotopensession": "/identification/site/",
  "urlusermanual":  "https://www.abcdesktop.io/",
  "urlusersupport": "https://www.abcdesktop.io/",
  "urlopensourceproject": "https://www.abcdesktop.io/"
}
```

##### Login progress

Login progress is from HTML `span` tags

```html
<span id='projectNameSplitedStagea'>a</span>
<span id='projectNameSplitedStageb'>b</span>
<span id='projectNameSplitedStagec'>c</span>
<span id='projectNameSplitedStaged'>desktop</span>
```


#### Colors dictionary entries

| entry          | default value  | example   |
|----------------|----------------|-----------|
| @primary       | #474B55        | #474B55   |
| @secondatry    | #2D2D2D        | #2D2D2D   |
| @tertiary      | #6EC6F0        | #6EC6F0   |

### Create a new `Dockerfile` to build changes

#### Update the ui.json with your own values

Change for example the name to

```
"name": "acmedesktop.io"
```

and the  

```
@tertiary "value": "#00BCD4"
```

Example

```json
{
  "name": "acmedesktop.io",
  "projectNameSplitedHTML": "<span id='projectNameSplitedStagea'>a</span><span id='projectNameSplitedStageb'>c</span><span id='projectNameSplitedStagec'>me</span><span id='p
rojectNameSplitedStaged'>desktop</span>",
  "colors": [
    {
      "name": "@x11bgcolor",
      "value": "#6EC6F0"
    },
    {
      "name": "@primary",
      "value": "#474B55"
    },
    {
      "name": "@secondary",
      "value": "#2D2D2D"
    },
    {
      "name": "@tertiary",
      "value": "#00BCD4"
    },
    {
      "name": "@quaternary",
      "value": "#1E1E1E"
    },
    {
      "name": "@svgColor",
      "value": "#FFFFFF"
    },
    {
      "name": "@danger",
      "value": "#CD3C14"
    },
    {
      "name": "@success",
      "value": "#32C832"
    },
    {
      "name": "@info",
      "value": "#527EDB"
    },
    {
      "name": "@warning",
      "value": "#FFCC00"
    },
    {
      "name": "@light",
      "value": "#FFFFFF"
    },
    {
      "name": "@dark",
      "value": "#666666"
    },
    {
      "name": "@blue",
      "value": "#4BB4E6"
    },
    {
      "name": "@green",
      "value": "#50BE87"
    },
    {
      "name": "@purple",
      "value": "#A885D8"
    },
    {
      "name": "@pink",
      "value": "#FFB4E6"
    },
    {
      "name": "@yellow",
      "value": "#FFD200"
    }
  ],
  "urlcannotopensession": "/identification/site/",
  "urlusermanual":  "https://www.abcdesktop.io/",
  "urlusersupport": "https://www.abcdesktop.io/",
  "urlopensourceproject": "https://www.abcdesktop.io/"
}
```


#### docker build

Run the docker build command to build the new `oc.nginx:acme` image
The target image is `abcdesktopio/oc.nginx:acme` you shoudl change it with your own for example `myacme/oc.nginx:acme`

```bash
docker build --build-arg NODE_MAJOR=20 --build-arg BASE_IMAGE=abcdesktopio/oc.nginx.builder --build-arg BASE_IMAGE_RELEASE=3.3 --build-arg TARGET=dev  -t abcdesktopio/oc.nginx:acme -f Dockerfile .
```

```bash
docker build --build-arg NODE_MAJOR=20 --build-arg BASE_IMAGE=abcdesktopio/oc.nginx.builder --build-arg BASE_IMAGE_RELEASE=3.3 --build-arg TARGET=prod  -t abcdesktopio/oc.nginx:acme -f Dockerfile .
[+] Building 16.5s (19/19) FINISHED                                                                                                                          docker:default
 => [internal] load build definition from Dockerfile                                                                                                                   0.0s
 => => transferring dockerfile: 962B                                                                                                                                   0.0s
 => [internal] load metadata for docker.io/library/nginx:latest                                                                                                        0.0s
 => [internal] load metadata for docker.io/abcdesktopio/oc.nginx.builder:3.3                                                                                           0.0s
 => [internal] load .dockerignore                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                        0.0s
 => CACHED [stage-1 1/2] FROM docker.io/library/nginx:latest                                                                                                           0.0s
 => CACHED [builder  1/11] FROM docker.io/abcdesktopio/oc.nginx.builder:3.3                                                                                            0.0s
 => [internal] load build context                                                                                                                                      0.1s
 => => transferring context: 265.27kB                                                                                                                                  0.1s
 => [builder  2/11] RUN echo current branch is                                                                                                                         0.2s
 => [builder  3/11] RUN echo NODE release is 20                                                                                                                        0.2s
 => [builder  4/11] RUN echo current target is prod it can be 'dev' or 'prod'                                                                                          0.2s
 => [builder  5/11] COPY . /var/webModules                                                                                                                             0.4s
 => [builder  6/11] WORKDIR /var/webModules                                                                                                                            0.1s
 => [builder  7/11] RUN make clean                                                                                                                                     0.7s
 => [builder  8/11] RUN make prod                                                                                                                                      9.7s
 => [builder  9/11] RUN ./mkversion.sh && cat version.json                                                                                                             0.2s
 => [builder 10/11] RUN /myenv/bin/html5validator index.html                                                                                                           2.0s 
 => [builder 11/11] RUN make removebuildtools                                                                                                                          0.8s 
 => [stage-1 2/2] COPY --from=builder /var/webModules /usr/share/nginx/html                                                                                            0.7s 
 => exporting to image                                                                                                                                                 0.7s 
 => => exporting layers                                                                                                                                                0.7s 
 => => writing image sha256:d7bdbc9f7fafe3282161551e84c5997bb12051bded6405190267863dd73a1698                                                                           0.0s
 => => naming to docker.io/abcdesktopio/oc.nginx:acme  
```

#### update the `abcdesktop.yaml`

To update the `abcdesktop.yaml` to replace `abcdesktopio/oc.nginx:3.3` by your own image `myacme/oc.nginx:acme`


- edit your own `abcdesktop.yaml` file

```
      [...]
      - name: nginx
        imagePullPolicy: Always
        image: abcdesktopio/oc.nginx:3.3
        ports:
          - containerPort: 80
            name: http
      [...]
```


Update the `deployement` with your new image name `abcdesktopio/oc.nginx:acme`

```
      [...]
      - name: nginx
        imagePullPolicy: Always
        image: abcdesktopio/oc.nginx:acme
        ports:
          - containerPort: 80
            name: http
      [...]
```

apply your abcdesktop.yaml file

```
kubectl apply -f abcdesktop.yaml
```




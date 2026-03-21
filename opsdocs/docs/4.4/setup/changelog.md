# Change log from 4.3 to 4.4


The prominent changes for this release are:

- `pyos` map roles to pod's labels. each role is added as pod label. Roles are read from user's groups (LDAP, ActiveDirectory or OAuth ) 
- `webmodule` new ful screen mode fully inspired from noVNC control bar
- `console` one line install from applist.json file from `ABCDESKTOP_APPLICATIONS_LIST_URL`
- `abcdesktop.yaml` add new configmap with `ABCDESKTOP_VERSION` and `ABCDESKTOP_APPLICATIONS_LIST_URL`

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: version-config
data:
  versionConfig.json: |-
    {
      "ABCDESKTOP_VERSION": "4.4",
      "ABCDESKTOP_APPLICATIONS_LIST_URL": "https://raw.githubusercontent.com/abcdesktopio/images/refs/heads/main/appLists/appList.4.4.json"
    }
---
```   
 

      

---
tags:
- read bu JFV
---

# How to request a new feature / report an issue ?
## How to request a feature ?
=======
- JFV
- AD
---

# Issue or feature request

## How to request a new feature ?
>>>>>>> 323f880427603366347a04ca06f973d2647cc32b

To create a new feature, please use the `conf` github repository, by following the link [Ask a feature](https://github.com/abcdesktopio/conf/issues)

- Describe what you are expecting
- Tag it as *feature* in field **type** on the right.


## How to report an issue ?

To create an issue, please use the `conf` github repository, by following the link [Create an issue](https://github.com/abcdesktopio/conf/issues)

- **Requirement** Add your `od.config` file

  Run the command line to get it

  ```bash
  NAMESPACE=abcdesktop
  kubectl -n $NAMESPACE get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
  ```

- **Requirement** Add your `abcdesktop.yaml` file
- Describe what you are expecting
- Describe what you get


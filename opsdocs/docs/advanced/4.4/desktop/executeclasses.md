# executeclasses 

The executeclasses defines the resources for the desktop pods and for applications.

## executeclasses dictionary

```
executeclasses : {
  'default':{
    'nodeSelector':None,
    'description': 'default: up to 4 CPU cores and 8Gi',
    'runtimeClassName': None,
    'resources':{
      'requests':{'memory':"576Mi",'cpu':"220m"},       
      'limits':  {'memory':"8Gi",'cpu':"4000m"}
    }
  },
  'bronze':{
    'nodeSelector':None,
    'runtimeClassName': None,
    'description': 'bronze: up to 2 CPU cores and 8Gi',
    'resources':{
      'requests':{'memory':"576Mi",'cpu':"220m"},
      'limits':  {'memory':"8Gi",'cpu':"2000m"}
    }
  },
  'silver':{
    'nodeSelector': None,
    'description': 'silver: 4 CPU cores and 32Gi RAM',
    'runtimeClassName': None,
    'resources':{
      'requests':{'memory':"2Gi",'cpu':"2000m"},       
      'limits':{'memory':"32Gi",'cpu':"4000m"} 
    }
  },
  'gold':{
    # give a gpu to graphical container
    'containers' : { 'graphical': { 'resources': { 'limits': { 'nvidia.com/gpu':'1' } } } },
    'nodeSelector':{'nvidia.com/gpu': 'true'},
    'description': 'gold: 4 CPU cores, 32Gi RAM and 1 GPU',
    'runtimeClassName': 'nvidia',
    'resources':{
      'requests':{'memory':"2Gi",'cpu':"4000m"},       
      'limits':  {'memory':"32Gi",'cpu':"4000m"}
    }
  },
  'platinum':{
    # give a gpu to graphical container
    'containers' : { 'graphical': { 'resources': { 'limits': { 'nvidia.com/gpu':'1' } } } },
    # nodeselector optional 
    'nodeSelector':{'nvidia.com/gpu': 'true'},
    # this appears only on web interface 
    'description': 'platinum: 8 CPU cores, 128G RAM and 1 GPU',
    'runtimeClassName': 'nvidia',
    'resources':{
      'requests':{'memory':"4Gi",'cpu':"4000m"},       
      'limits':{'memory':"128Gi",'cpu':"8000m"} 
    }
  }}
```

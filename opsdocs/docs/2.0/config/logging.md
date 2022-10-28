
# Logging configuration in od.config


The ```logging``` configuration is a dictionnary object. The logging configuration describes where and how log message information have to been send.

```logging``` dict use the python logging module [logging module](https://docs.python.org/3.8/library/logging.config.html)

The ```syslog``` and ```graylog``` protocol messaging are supported too.

The default features for each handlers are : 


| handler              | Features   |
|--------------------|-------------|
|  ```console```   		| log message using a ```logging.StreamHandler``` to the stream:  ```ext://sys.stdout ``` formated as standard |
|  ```cherrypy_console``` | log message using a ```logging.StreamHandler``` to the stream:  ```ext://sys.stdout ``` formatted as access | 
|  ```cherrypy_access```  | log message using a ```logging.StreamHandler``` to the file stream ```logs/access.log``` formatted as access  |
|  ```cherrypy_trace```  | log message using a ```logging.StreamHandler``` to the stream:  ```logs/trace.log``` formatted as standard |  





Sub modules used by od.py can log information too. 

| Sub module                    | Default Values              |
|-------------------------------|-----------------------------|
|  ```docker.utils.config```    | ```{ 'level': 'INFO' },```  |
|  ```urllib3.connectionpool``` | ```{ 'level': 'ERROR'},```  | 



The ```logging``` sample configuration :

```
#              
# logging configuration 
# come from https://docs.python.org/3.8/library/logging.config.html
# need double %% to escape %
# 
# graylog https://github.com/severb/graypy
# use handler class name as
# graypy.GELFUDPHandler - UDP log forwarding
# graypy.GELFTCPHandler - TCP log forwarding
# graypy.GELFTLSHandler - TCP log forwarding with TLS support
# graypy.GELFHTTPHandler - HTTP log forwarding
# graypy.GELFRabbitHandler - RabbitMQ log forwarding

logging: {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'access': {
      'format': '%%(message)s - user: %%(userid)s',
      'datefmt': '%%Y-%%m-%%d %%H:%%M:%%S'
    },
    'standard': {
      'format': '%%(asctime)s %%(module)s [%%(levelname)-7s] %%(name)s.%%(funcName)s:%%(userid)s %%(message)s',
      'datefmt': '%%Y-%%m-%%d %%H:%%M:%%S'
    },
    'syslog': {
      'format': '%%(asctime)s %%(levelname)s %%(module)s %%(process)d %%(name)s.%%(funcName)s:%%(userid)s %%(message)s',
      'datefmt': '%%Y-%%m-%%d %%H:%%M:%%S'
    },
    'graylog': {
      'format': '%%(levelname)s %%(module)s %%(process)d %%(name)s.%%(funcName)s:%%(userid)s %%(message)s'      
    }
  },
  'filters': {
    'odcontext': {
      '()': 'oc.logging.OdContextFilter'
    }
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'filters': [ 'odcontext' ],
      'formatter': 'standard',
      'stream': 'ext://sys.stdout'
    },
    'cherrypy_console': {
      'class': 'logging.StreamHandler',
      'filters': [ 'odcontext' ],
      'formatter': 'access',
      'stream': 'ext://sys.stdout'
    },
    'cherrypy_access': {
      'class': 'logging.handlers.RotatingFileHandler',
      'filters': [ 'odcontext' ],
      'formatter': 'access',
      'filename': 'logs/access.log',
      'maxBytes': 10485760,
      'backupCount': 20,
      'encoding': 'utf8'
    },
    'cherrypy_trace': {
      'class': 'logging.handlers.RotatingFileHandler',
      'filters': [ 'odcontext' ],
      'formatter': 'standard',
      'filename': 'logs/trace.log',
      'maxBytes': 10485760,
      'backupCount': 20,
      'encoding': 'utf8',
      'mode': 'w'
    }
  },
  'loggers': {
    '': {
      'handlers': [ 'console', 'cherrypy_trace'  ],
      'level': 'DEBUG'
    },
    'docker.utils.config': {
      'level': 'INFO'
    },
    'urllib3.connectionpool': {
      'level': 'ERROR'
    },
    'cherrypy.access': {
      'handlers': [ 'cherrypy_access' ],
      'level': 'INFO',
      'propagate': False
    },
    'cherrypy.error': {
      'handlers': [ 'console', 'cherrypy_trace' ],
      'level': 'ERROR',
      'propagate': False
    }
  } }
```

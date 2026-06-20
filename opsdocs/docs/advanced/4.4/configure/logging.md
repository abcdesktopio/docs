
# Logging Configuration in od.config

The `logging` configuration is a dictionary object that specifies where and how log messages are sent.

The `logging` dictionary follows the Python logging module configuration format. Refer to the [logging module](https://docs.python.org/3.8/library/logging.config.html) documentation for the full specification.

The `syslog` and `graylog` protocols are also supported for remote log forwarding.



## Limits

For HTTP responses only, each log line is limited by default to 2048 bytes.

In `od.config`, the `max_log_body_size` parameter is set to `2048` by default:

```
max_log_body_size: 2048
```

Adjust this value to increase or decrease the maximum length of a log line.


If a log line exceeds `max_log_body_size`, the string `[truncated]` replaces the end of the line:

```abcsrv23
2026-05-05 13:41:09 abcsrv23 132131221128896 od [INFO   ] __main__.trace_response:anonymous /core/getkeyinfo b'{"id": {"ephemeral_container": f...[truncated]'
2026-05-05 13:41:09 abcsrv23 132131237914304 orchestrator [DEBUG  ] oc.od.orchestrator.ODOrchestratorKubernetes.__init__:leela load_kube_config done
2026-05-05 13:41:09 abcsrv23 132131195950784 od [INFO   ] __main__.trace_response:anonymous /core/getkeyinfo b'{"id": null, "callbackurl": null...[truncated]'
2026-05-05 13:41:09 abcsrv23 132131237914304 orchestrator [DEBUG  ] oc.od.orchestrator.ODOrchestratorKubernetes.findDesktopByUser:leela 
2026-05-05 13:41:09 abcsrv23 132131237914304 orchestrator [DEBUG  ] oc.od.orchestrator.ODOrchestratorKubernetes.findPodByUser:leela 
2026-05-05 13:41:09 abcsrv23 132131237914304 orchestrator [DEBUG  ] oc.od.orchestrator.ODOrchestratorKubernetes.findDesktopByUser:leela Pod is found leela-be51a
```

## Logging Configuration

The `logging` dictionary uses the Python logging module configuration format. Refer to the [logging module](https://docs.python.org/3.8/library/logging.config.html) documentation for the full specification.

The `syslog` and `graylog` protocols are also supported.

The default configuration for each handler is as follows:


| handler              | Features   |
|--------------------|-------------|
|  `console`   		| log message using a `logging.StreamHandler` to the stream:  `ext://sys.stdout ` formated as standard |
|  `cherrypy_console` | log message using a `logging.StreamHandler` to the stream:  `ext://sys.stdout ` formatted as access | 
|  `cherrypy_access`  | log message using a `logging.StreamHandler` to the file stream `logs/access.log` formatted as access  |
|  `cherrypy_trace`  | log message using a `logging.StreamHandler` to the stream:  `logs/trace.log` formatted as standard |  




Sub-modules used by `od.py` also emit log messages.

| Sub module                    | Default Values              |
|-------------------------------|-----------------------------|
|  `docker.utils.config`    | `{ 'level': 'INFO' },`  |
|  `urllib3.connectionpool` | `{ 'level': 'ERROR'},`  | 



The following is a sample `logging` configuration:

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
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
      'access': {
        'format': '%%(message)s - user: %%(userid)s',
        'datefmt': '%%Y-%%m-%%d %%H:%%M:%%S'
      },
      'standard': {
        'format': '%%(asctime)s %%(nodename)s %%(thread)d %%(module)s [%%(levelname)-7s] %%(name)s.%%(funcName)s:%%(userid)s %%(message)s',
        'datefmt': '%%Y-%%m-%%d %%H:%%M:%%S'
      },
      'syslog': {
        'format': '%%(asctime)s %%(nodename)s %%(thread)s %%(levelname)s %%(module)s %%(process)d %%(name)s.%%(funcName)s:%%(userid)s %%(message)s',
        'datefmt': '%%Y-%%m-%%d %%H:%%M:%%S'
      },
      'graylog': {
        'format': '%%(levelname)s %%(nodename)s %%(thread)s %%(module)s %%(process)d %%(name)s.%%(funcName)s:%%(userid)s %%(message)s'      
      }
    },
    'filters': {
      'odcontext': {
        '()': 'oc.logging.OdContextFilter'
      }
    },
    'handlers': {
      'stdout': {
        'class': 'logging.StreamHandler',
        'filters': [ 'odcontext' ],
        'level': 'DEBUG',
        'formatter': 'standard',
        'stream': 'ext://sys.stdout'
      },
      'stderr': {
        'class': 'logging.StreamHandler',
        'filters': [ 'odcontext' ],
        'level': 'ERROR',
        'formatter': 'standard',
        'stream': 'ext://sys.stderr'
      },
      'trace': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'DEBUG',
        'filters': [ 'odcontext' ],
        'formatter': 'standard',
        'filename': 'logs/trace.log',
        'maxBytes': 10485760,
        'backupCount': 20,
        'encoding': 'utf8',
        'mode': 'w'
      },
      'cherrypy_access': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filters': [ 'odcontext' ],
        'formatter': 'access',
        'filename': 'logs/access.log',
        'maxBytes': 10485760,
        'backupCount': 20,
        'encoding': 'utf8'
      }
    },
    'loggers': {
      # dedicated python modules 
      'urllib3.connectionpool': {
        'level': 'ERROR',
      },
      'kubernetes': {
        'handlers': [ 'stderr', 'stdout',  'trace' ],
        'level': 'ERROR',
        'propagate': False
      },
      'cherrypy.access': {
        'handlers': [ 'cherrypy_access' ],
        'level': 'INFO',
        'propagate': False
      },
      'requests_oauthlib' : {
        'handlers': [ 'stderr', 'stdout',  'trace' ],
        'level': 'ERROR',
        'propagate': False
      },
      'cherrypy' : {
        'handlers': [ 'stderr', 'stdout',  'trace' ],
        'level': 'ERROR',
      }
    },
    'root': {
      # put the level to 'DEBUG', each handler fix the level value
      'level': 'DEBUG',
      'handlers': [ 'stderr', 'stdout',  'trace' ]
    }}

```

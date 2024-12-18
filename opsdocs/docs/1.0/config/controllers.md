
# Controllers 

## Controllers
abcdesktop.io use a Model–view–controller (usually known as MVC) is a software design pattern commonly used for developing user interfaces which divides the related program logic into three interconnected elements. This is done to separate internal representations of information from the ways information is presented to and accepted from the user.


| Controller                  |  Description   |
|-----------------------------|--------------- |
|```AccountingController``` 	| accounting data json and ebnf format |
|```AuthController```			| authenticate user  |
|```ComposerController``` 		| CRUD main services (like createDesktop, runApplication)|
|```CoreController```			| get configuration and user message info |
|```ManagerController``` 		| manage pyos |
|```PrinterController```		| CRUD printer object |
|```StoreController```			| CRUD key value data  |
|```UserController```			| retrieve user information |


## Access Permission

The ```AccountingController``` and ```ManagerController``` access is protected with a source ip address filter.
The access control filter is defined in a dictionary.
Each dictionary entry use the ```controller``` name and with an entry ```permitip```.
The ```permitip``` is a list of subnet, for example ```[ '10.0.0.0/8', '172.16.0.0/12' ]```.
If ```permitip``` is not set or the ```controller``` name is not set, all ip source address are allowed the send a request to the controller.

The ```controllers``` dictionnary is defined in the ```od.config``` file. 
By default the configuration permit private network defined in [rfc1918](https://tools.ietf.org/html/rfc1918) and [rfc4193](https://tools.ietf.org/html/rfc4193). Get more information about the [private network](https://en.wikipedia.org/wiki/Private_network).

By default others controllers access is enabled, without ip restriction.


```
	controllers : { 
		'AccountingController': 
			{ 
				'permitip': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', '169.254.0.0/16', '127.0.0.0/8' ] 
			},
		'AuthController' : 		{ 'permitip': None },
		'ComposerController' : 	{ 'permitip': None },
		'CoreController' : 		{ 'permitip': None },
		'ManagerController': 
			{ 
				'permitip': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', '169.254.0.0/16', '127.0.0.0/8' ] 
			},
		'PrinterController' : 	{ 'permitip': None },
		'StoreController' : 	{ 'permitip': None },
		'UserController' : 		{ 'permitip': None }
	} 
```


If the source ip address is not allowed, the response is a HTTP status ```code 403 Forbidden```
	
```
{"status": 403, "status_message": "403 Forbidden", "message": "Request forbidden -- authorization will not help"} 
```

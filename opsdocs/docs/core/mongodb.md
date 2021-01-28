# Mongodb


[Mongodb](https://www.mongodb.org) is an open-source document database that provides high performance, high availability, and automatic scaling
The [mongodb container](https://hub.docker.com/_/mongo/) comes from the public docker registry. This service is attend to the netback network.

## Collections

abcdesktop.io uses the colections mongodb to store 

- webrtc call history 
- login history 
- dock web state

### dock state

The dock state is stored as an array of application name. The dock state is stored when the user changes it (for exemplate add or remove an application inside the dock zone ). The collection's name is the userid. The key's name is 'dock'


```
[ 
 	"keyboard",
	"frontendjs.filemanager",
	"Mail.Thunderbird",
	"libreoffice.libreoffice-calc",
	"libreoffice.libreoffice-writer",
	"Navigator.Firefox",
	"gimp.Gimp",
	"gnome-terminal.Gnome-terminal"
]
```

### loginHistory

login History is an object collection. One collection is created for each user. 
The collection's name is the userid. The javascript code can only read and NEVER write data to the loginHistory collection.

The object's format is :

```
{
 "picture":"https://scontent.xx.fbcdn.net/v/t1.0-1/p480x480/1452008_10202217750222019_1258804247_n.jpg?oh=a96b2290e63e1e81525ede1a5b073853&oe=59184A75",
 "sub":"10208942501856324",
 "ipaddr":"181.125.208.3, 10.255.0.3",
 "provider":"facebook",
 "date":"2017-01-12 11:19:57.946554",
 "useragent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
 "_id":"5877665d0790160b0d59efd0",
 "name":"Alexandre Devely"}
```

- _id : is the mongodb id
- sub : is the userid
- ipaddr : is the client ip address
- provider : authenticated provider 
- date : date formated 
- useragent : user browser description
- name : the user name  

#### method 

To getCollection data, javascript code ask the os.py service using a XMLHTTPRequest
 
getCollection 'loginHistory' is called by whoami.js 

```
 getCollection('loginHistory', function(msg) {
            if (msg.status === 200) {
                var history = msg.result;
                loginHistory = history;
                buildHtmlTable(history);
            }
        })
```
 

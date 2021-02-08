# pyos

![Update oc.pyos](https://github.com/abcdesktopio/oc.pyos/workflows/Update%20oc.pyos/badge.svg)

oc.pyos is the application server for abcdesktop.io. 
os.py is python script based on cherrypy framework and listen tcp port 8000.
os.py daemon waits for json request from the javascript web client scripts, and implements methods : 

- 'login' : Request a login session, create a new user container if it does not exist.         
- 'getkeyinfo' : Return the public key from a provider        
- 'logout'  : logout the container
- 'logs' : return logs from a started container
- 'getapplist' : return all avalaible applications
- 'install' : [ deprecated ] install a package
- 'share' : send a auth token to the email to share the desktop 
- 'support' : send a support request
- 'restart' : retart the user container           
- 'ocrun' : start a application             
- 'ocstop' : stop the container
- 'whoami' : return a JSON object whoami         
- 'set' : set a key value 
- 'get' : get value from a key  
- 'setcollection' : add value to a collection
- 'getcollection' : get all values from a collection


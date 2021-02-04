# dock configuration in od.config

# Menu Setting


The menu can be changed using the dictionnary object ```menuconfig```

```
menuconfig : {
				 	'settings'	: True, 
					'appstore'	: True, 
					'screenshot'	: True, 
					'download'	: True, 
					'logout'		: True, 
					'disconnect'	: True 
}
```


# default dock config

The dock session in od.config file describe the default docker in abcdesktop.io.
The default dock value contains the default applications.
The ```dock``` option is a dictionnary read by the front web as a json object.



| docker entry       | Descriptions   |
|--------------------|-------------|
|  ```filemanager ```   		| FileManager application  |
|  ```terminal ``` | Terminal application | 
|  ```webshell ```  | HTML 5, terminal application based on xterm.js  |

[comment]: |  ```webshorcut```  | Web browser url launch inside the container| 

  

```
dock : {        'filemanager':  {       'args': None,
                                        'showinview': u'dock',
                                        'name': u'FileManager',
                                        'keyword': u'files,file manager',
                                        'launch': u'nautilus.Nautilus',
                                        'displayname': u'FileManager',
                                        'execmode': u'builtin',
                                        'cat': u'utilities,office',
                                        'id': u'filemanager.d',
                                        'icon': u'pantheon-files-icons.svg' },

                'terminal':     {       'args': '',
                                        'name': u'TerminalBuiltin',
                                        'keyword': u'terminal,shell,bash,builtin,pantheon',
                                        'launch': u'qterminal.qterminal',
                                        'displayname': u'Terminal Builtin',
                                        'execmode': u'builtin',
                                        'cat': u'utilities,development',
                                        'id': u'terminalbuiltin.d',
                                        'hideindock': True,
                                        'icon': u'pantheon-terminal-builtin-icons.svg' },
                                        
                'webshell':     {       'name': u'WebShell',
                                        'keyword': u'terminal,shell,webshell,bash',
                                        'launch': u'frontendjs.webshell',
                                        'displayname': u'Web Shell',
                                        'execmode': u'frontendjs',
                                        'cat': u'utilities,development',
                                        'id': u'webshell.d',
                                        'icon': u'webshell.svg' }
}
```
  
## Additional applications 

This feature is deprecated.

To run embeded application inside the oc.user image container, with specific attribut ```{ 'execmode': 'builtin' }``` add 

```
'webshortcut':  {	'name': u'xlogo',
                    'showinview': u'dock',
                    'keyword': u'xlogo',
                    'execmode': u'builtin',
                    'launch': u'/usr/bin/xlogo',
                    'displayname': u'xlogo',
                    'execmode': u'builtin',
                    'cat': u'utilities',
                    'id': u'xlogo.d',
                    'icon': u'xlogo.svg',
                    'hideindock': False,
                    'args': '' 
}
```                                       
                                       
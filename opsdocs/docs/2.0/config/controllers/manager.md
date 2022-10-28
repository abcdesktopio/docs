
# ManagerController

## HTTP Request
 
The http request path is ```/API/manager```

| Path                                 | Params      | Response type |
|--------------------------------------|-------------|---------------| 
|  ```/API/manager/buildapplist```  | None        | Json object   |
|  ```/API/manager/updateactivedirectorysite```  | None        | Json object   |
|  ```/API/manager/garbagecollector```  | expirein=, force=False    | Json object   |
		
			
### buildapplist

```buildapplist``` ask pyos to list all abcdesktop.io docker image. Each docker image must have the specified label ```type=apps```. abcdesktop.io 

| Params            | Type        | Description        |
|-------------------|-------------|--------------------| 
|  None   | None     | None   |

example :

```
curl http://localhost/API/manager/buildapplist
```

Return the complete array if json images objects ready to run.


```
{"abcdesktopio/writer.d:latest": {"id": "abcdesktopio/writer.d:latest", "rules": null, "acl": null, "launch": "libreoffice.libreoffice-writer", "name": "Writer", "icon": "libreoffice-writer.svg", "keyword": "libre office writer,office,writer", "uniquerunkey": "libreoffice", "cat": "office", "args": "--writer", "execmode": null, "memory": null, "shm_size": null, "oomkilldisable": null, "showinview": "dock", "displayname": "Writer", "mimetype": ["application/vnd.oasis.opendocument.text", "application/vnd.oasis.opendocument.text-template", "application/vnd.oasis.opendocument.text-web", "application/vnd.oasis.opendocument.text-master", "application/vnd.oasis.opendocument.text-master-template", "application/vnd.sun.xml.writer", "application/vnd.sun.xml.writer.template", "application/vnd.sun.xml.writer.global", "application/msword", "application/vnd.ms-word", "application/x-doc", "application/x-hwp", "application/rtf", "text/rtf", "application/vnd.wordperfect", "application/wordperfect", "application/vnd.lotus-wordpro", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-word.document.macroenabled.12", "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "application/vnd.ms-word.template.macroenabled.12", "application/vnd.stardivision.writer-global", "application/x-extension-txt", "application/x-t602", "application/vnd.oasis.opendocument.text-flat-xml", "application/x-fictionbook+xml", "application/macwriteii", "application/x-aportisdoc", "application/prs.plucker", "application/vnd.palm", "application/clarisworks", "application/x-sony-bbeb", "application/x-abiword", "application/x-iwork-pages-sffpages", "application/x-mswrite"], "path": "/usr/lib/libreoffice/program/soffice", "desktopfile": "libreoffice-writer.desktop", "executablefilename": "soffice", "usedefaultapplication": true, "fileextensions": ["sxw", "stw", "doc", "dot", "wps", "rtf", "602", "wpd", "docx", "docm", "dotx", "dotm", "abw", "zabw", "pages", "dummy", "lrf", "cwk", "hqx", "fb2", "mw", "mcw", "mwd", "pdb", "wn"], "legacyfileextensions": ["odf", "ott", "fodt", "uot"]}, "abcdesktopio/math.d:latest": {"id": "abcdesktopio/math.d:latest", "rules": null, "acl": null, "launch": "libreoffice.libreoffice-math", "name": "Math", "icon": "libreoffice-math.svg", "keyword": "libre office math,office,math", "uniquerunkey": "libreoffice", "cat": "office", "args": "--math", "execmode": null, "memory": null, "shm_size": null, "oomkilldisable": null, "showinview": null, "displayname": "Math", "mimetype": ["application/vnd.oasis.opendocument.formula", "application/vnd.sun.xml.math", "application/vnd.oasis.opendocument.formula-template", "text/mathml", "application/mathml+xml"], "path": "/usr/lib/libreoffice/program/soffice", "desktopfile": "libreoffice-math.desktop", "executablefilename": "soffice", "usedefaultapplication": true, "fileextensions": ["odf", "odc"], "legacyfileextensions": ["odf", "odc"]}, "abcdesktopio/impress.d:latest": {"id": "abcdesktopio/impress.d:latest", "rules": null, "acl": null, "launch": "libreoffice.libreoffice-impress", "name": "Impress", "icon": "libreoffice-impress.svg", "keyword": "libre office impress,office,impress", "uniquerunkey": "libreoffice", "cat": "office", "args": "--impress", "execmode": null, "memory": null, "shm_size": null, "oomkilldisable": null, "showinview": "dock", "displayname": "Impress", "mimetype": ["application/vnd.oasis.opendocument.presentation", "application/vnd.oasis.opendocument.presentation-template", "application/vnd.sun.xml.impress", "application/vnd.sun.xml.impress.template", "application/mspowerpoint", "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.ms-powerpoint.presentation.macroenabled.12", "application/vnd.openxmlformats-officedocument.presentationml.template", "application/vnd.ms-powerpoint.template.macroenabled.12", "application/vnd.openxmlformats-officedocument.presentationml.slide", "application/vnd.openxmlformats-officedocument.presentationml.slideshow", "application/vnd.ms-powerpoint.slideshow.macroenabled.12", "application/vnd.oasis.opendocument.presentation-flat-xml", "application/x-iwork-keynote-sffkey"], "path": "/usr/lib/libreoffice/program/soffice", "desktopfile": "libreoffice-impress.desktop", "executablefilename": "soffice", "usedefaultapplication": true, "fileextensions": ["odp", "pot", "potm", "potx", "pps", "ppsx", "ppt", "pptx", "pptm"], "legacyfileextensions": ["odp"]}, "abcdesktopio/calc.d:latest": {"id": "abcdesktopio/calc.d:latest", "rules": null, "acl": null, "launch": "libreoffice.libreoffice-calc", "name": "Calc", "icon": "libreoffice-calc.svg", "keyword": "libre office calc,office,calc", "uniquerunkey": "libreoffice", "cat": "office", "args": "--calc", "execmode": null, "memory": null, "shm_size": null, "oomkilldisable": null, "showinview": "dock", "displayname": "Calc", "mimetype": ["application/vnd.oasis.opendocument.spreadsheet", "application/vnd.oasis.opendocument.spreadsheet-template", "application/vnd.sun.xml.calc", "application/vnd.sun.xml.calc.template", "application/msexcel", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel.sheet.macroenabled.12", "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "application/vnd.ms-excel.template.macroenabled.12", "application/vnd.ms-excel.sheet.binary.macroenabled.12", "text/csv", "application/x-dbf", "text/spreadsheet", "application/csv", "application/excel", "application/tab-separated-values", "application/vnd.lotus-1-2-3", "application/vnd.oasis.opendocument.chart", "application/vnd.oasis.opendocument.chart-template", "application/x-dbase", "application/x-dos_ms_excel", "application/x-excel", "application/x-msexcel", "application/x-ms-excel", "application/x-quattropro", "application/x-123", "text/comma-separated-values", "text/tab-separated-values", "text/x-comma-separated-values", "text/x-csv", "application/vnd.oasis.opendocument.spreadsheet-flat-xml", "application/vnd.ms-works", "application/x-iwork-numbers-sffnumbers"], "path": "/usr/lib/libreoffice/program/soffice", "desktopfile": "libreoffice-calc.desktop", "executablefilename": "soffice", "usedefaultapplication": true, "fileextensions": ["ods", "ots", "sxc", "stc", "fods", "uos", "uof", "xml", "xlsx", "xlsm", "xltm", "xltx", "xlsb", "xls", "xlm", "xlc", "xlw", "xlk", "xlt", "dif", "dbf", "htm", "html", "wk1", "wks", "123", "wb2", "rtf", "slk", "sylk", "csv", "numbers", "dummy", "cwk", "wps", "wk3", "wq1", "wq2"], "legacyfileextensions": ["ods", "ots", "csv"]}, "abcdesktopio/base.d:latest": {"id": "abcdesktopio/base.d:latest", "rules": null, "acl": null, "launch": "libreoffice.libreoffice-base", "name": "Base", "icon": "libreoffice-base.svg", "keyword": "libre office base,office,base", "uniquerunkey": "libreoffice", "cat": "development", "args": "--base", "execmode": null, "memory": null, "shm_size": null, "oomkilldisable": null, "showinview": null, "displayname": "Base", "mimetype": ["application/vnd.oasis.opendocument.database", "application/vnd.sun.xml.base"], "path": "/usr/lib/libreoffice/program/soffice", "desktopfile": "libreoffice-base.desktop", "executablefilename": "soffice", "usedefaultapplication": true, "fileextensions": ["odb"], "legacyfileextensions": ["odb"]}}

```




### updateactivedirectorysite

| Params            | Type        | Description        |
|-------------------|-------------|--------------------| 
|  None   | None     | None   |

example :

```
curl http://localhost/API/manager/updateactivedirectorysite
```

### garbagecollector

| Params            | Type        | Description        |
|-------------------|-------------|--------------------| 
|  ```expirein```   | integer     | number in seconds since the container create date time   |
|  ```force```      | boolean     | garbage the container even if a user is connected       |


example :

```
curl "http://localhost/API/manager/garbagecollector?expirein=9473"
curl "http://localhost/API/manager/garbagecollector?expirein=9473&force=True"
```

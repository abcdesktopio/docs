
# JIRA configuration 

abcdesktop.io support JIRA 

## JIRA option

In ```od.config``` add the ```jira``` option.
```jira``` option is a dictionary with the entries :


| entry      | sample value			                        |
|------------|-----------------------------------------------|
| url 		   | https://domainexample.atlassian.net/          |
| project_id | ABCD                                          |
| username	| account@domain.local                          |
| apikey 	   | XXXXXXXXXXXXXXXXXXXX                          |
 

And fill the dictionary 

```
jira : { 
			'url': 			'https://domainexample.atlassian.net/',
         	'project_id': 	'ABCD',
         	'username': 	'account@domain.local',
         	'apikey' : 		'XXXXXXXXXXXXXXXXXXXX' }
```

Then apply the new configuration file ```od.config``` by retrasting the daemon.


When ```jira``` option is set, a new icon ```issue``` appears at the top.

![issue front web icon](img/jira-enable-front.png)

Click on the ```issue``` icon, a new window is appear.

![new issue jira](img/jira-new-issue.png)

Fill ```Summary``` and ```Your Report``` values

![new issue jira](img/jira-fill-issue.png)

Then press the ```Send``` button. A notification message appears on the left top corner.

![fill issue jira](img/jira-issue-submit-done.png)

Log into your jira server, and check your backlog 
 
![fill issue jira](img/jira-backlog-issue.png)

Great you added a new issue tracking.


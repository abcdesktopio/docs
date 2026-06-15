# FRNOG 42

![FRNOG logo](img/frnog.png)

The FRench Network Operators Group ([FRnOG](http://www.frnog.org)) brings together people interested in security, research, and Internet operations in France for information exchange.

This page provides materials from the session held on Friday, October 24, 2025 at [FRnOG 42](https://www.frnog.org/?page=frnog42).

## Slide Content

- PDF format [download file](abcdesktop-frnog.pdf)

## Video Content

- Demo abcdesktop frnog 42

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/dq3bcFu5pr8" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>


### Description

- Login credentials (`Philip J. Fry`,`fry`)
- Create a pod desktop with all containers
- Start the terminal application
- Run `kubectl get pods -n abcdesktop`
  - Show current user pod for `fry`
- Start the Firefox application
  - Browse for a video on the `http://culturepub.fr` website
- Start the Qterminal application as a pod
	- Run the `top` command to show processes
- Run `kubectl get pods -n abcdesktop` again in terminal
- Run `kubectl delete pods fry-qterminal-app-XXXX -n abcdesktop` again in terminal
- Logoff


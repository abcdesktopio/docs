# FRnOG 42 — abcdesktop.io Presentation

![FRNOG logo](img/frnog.png)

The French Network Operators Group ([FRnOG](http://www.frnog.org)) is an open community that brings together network engineers, security researchers, and Internet operations professionals in France for technical knowledge exchange.

This page provides materials from the abcdesktop.io session presented on Friday, October 24, 2025, at [FRnOG 42](https://www.frnog.org/?page=frnog42). The session covered the abcdesktop.io platform's core security architecture, including **Remote Browser Isolation (RBI)** and **Remote Application Isolation (RAI)**, and demonstrated live deployment on a Kubernetes cluster.

## Slides

- PDF format: [download file](abcdesktop-frnog.pdf)

## Demo Video

The following video demonstrates a live abcdesktop.io session recorded during the FRnOG 42 presentation:

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/dq3bcFu5pr8" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

### Demo Walkthrough

The demo uses the following credentials: username `Philip J. Fry`, password `fry`.

1. **Authentication** — Log in to abcdesktop.io using the preconfigured LDAP account `fry`.
2. **Pod provisioning** — A user desktop pod is created with all service containers (graphical, printer, sound, filer).
3. **Terminal application** — Launch the terminal application and run `kubectl get pods -n abcdesktop` to display the running user pod for `fry`.
4. **Remote Browser Isolation demo** — Launch the Firefox application. This demonstrates RBI: Firefox runs entirely inside an isolated container on the Kubernetes node; only rendered pixels are streamed to the client browser. Browse to `http://culturepub.fr` to play a video.
5. **Remote Application Isolation demo** — Launch the Qterminal application as a separate pod. This demonstrates RAI: the terminal emulator runs in a dedicated, isolated container namespace. Run the `top` command inside the Qterminal to display live process information.
6. **Pod lifecycle verification** — In the main terminal, run `kubectl get pods -n abcdesktop` again to show both the user desktop pod and the isolated Qterminal application pod.
7. **Ephemeral container teardown** — Run `kubectl delete pods fry-qterminal-app-XXXX -n abcdesktop` to terminate the Qterminal application pod, demonstrating the ephemeral nature of application containers.
8. **Session termination** — Log off from abcdesktop.io.

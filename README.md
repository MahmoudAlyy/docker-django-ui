# docker-django-ui
A simple web UI for managing docker containers & images and interacting with using a fully functional terminal using django, socket.io & xterm.js 

You can start, stop or remove containers,

![Imgur](https://i.imgur.com/voZECmr.png)

attach to a container using a fully functional terminal,

![screenshot](https://github.com/MahmoudAlyy/docker-django-ui/blob/main/docker-django-ui.gif)

browse docker hub and pull new images &

![Imgur](https://i.imgur.com/MEG3mUA.gif)

launch or remove images.

![Imgur](https://i.imgur.com/1iUzvR3.png)




# Installation
Clone the repository and cd into it, then run:
```
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python manange.py runserver

wsgi starting up on http://127.0.0.1:8000
```

  

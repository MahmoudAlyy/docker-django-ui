# docker-django-ui
A simple web UI for managing docker containers and images using django, socket.io and xterm.js

You can start, stop or remove containers,

![Imgur](https://i.imgur.com/voZECmr.png)


launch or remove images,

![Imgur](https://i.imgur.com/1iUzvR3.png)

browse docker hub and pull new images

![Imgur](https://i.imgur.com/MEG3mUA.gif)

or console into them using a fully functional terminal

![screenshot](https://github.com/MahmoudAlyy/docker-django-ui/blob/main/docker-django-ui.gif)


# Installation
Clone the repository and cd into it, then run:
```
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python manange.py runserver

wsgi starting up on http://127.0.0.1:8000
```

  

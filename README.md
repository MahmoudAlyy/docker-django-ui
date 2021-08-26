# docker-django-ui
A simple web UI for managing docker containers & images and interacting with using a fully functional terminal using django, socket.io & xterm.js 

Live demo : http://35.224.213.24/

You can start, stop or remove containers,

![screenshot](https://github.com/MahmoudAlyy/docker-django-ui/blob/main/readme_images/docker-django-ui-containers.jpeg)


attach to a container using a [fully functional terminal](https://github.com/MahmoudAlyy/django-xtermjs/ "django-xtermjs"),



![screenshot](https://github.com/MahmoudAlyy/docker-django-ui/blob/main/readme_images/docker-django-ui.gif)

browse docker hub and pull new images &

![screenshot](https://github.com/MahmoudAlyy/docker-django-ui/blob/main/readme_images/docker-django-browse.gif)


launch or remove images.

![screenshot](https://github.com/MahmoudAlyy/docker-django-ui/blob/main/readme_images/docker-django-ui-images.gif)





# Installation
Clone the repository and cd into it, then run:
```
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python manange.py runserver

wsgi starting up on http://127.0.0.1:8000
```
**Note**:
    Docker daemon must be running.


# TODO
- [x] Add bootstrap to the frontend.
- [x] Dockerize the app and host a live demo.
- [ ] Use celery and redis to make container operation asynchronous. 







# docker-django-ui
A simple web UI for managing docker containers & images and interacting with using a fully functional terminal using django, celery, redis, socket.io, xterm.js & bootstrap.

Live demo : http://35.223.46.5

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
docker-compose up
```
**Note**:
    Docker daemon must be running.


# TODO
- [x] Add bootstrap to the frontend.
- [x] Dockerize the app and host a live demo.
- [x] Use celery and redis to make container operation asynchronous. 
- [ ] Use eventsource/websockets to retreive updates from server.




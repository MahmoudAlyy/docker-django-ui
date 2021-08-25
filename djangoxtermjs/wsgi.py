"""
WSGI config for djangoxtermjs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
import eventlet
import eventlet.wsgi

from xterm.views import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoxtermjs.settings')

django_app = get_wsgi_application()

#sio = socketio.Server(async_mode='eventlet')

#application = socketio.Middleware(sio, django_app)
application = socketio.WSGIApp(sio, django_app)

eventlet.wsgi.server(eventlet.listen(('', 8000)), application)

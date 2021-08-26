"""
WSGI config for djangoxtermjs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoxtermjs.settings'

import socketio
import eventlet
import eventlet.wsgi

from xterm.views import sio
from djangoxtermjs.settings import static_files

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoxtermjs.settings')

from django.core.wsgi import get_wsgi_application

django_app = get_wsgi_application()

#serve statif file
application = socketio.WSGIApp(sio, django_app,static_files=static_files)

eventlet.wsgi.server(eventlet.listen(('', 80)), application)

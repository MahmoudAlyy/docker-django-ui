import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import socketio
import pty
import select
import subprocess
import struct
import fcntl
import termios 
import signal
import eventlet
import docker
import time

import json
from .models import *

async_mode = "eventlet"
sio = socketio.Server(async_mode=async_mode)

def index(request):
		client = docker.from_env()
		return render(request, 'index.html',{'containers':client.containers.list(all=True),'images':client.images.list(),'info':client.info()})

def create(request):
	if request.method == 'POST':
		client = docker.APIClient()
		name = json.load(request)['name']
		container = client.create_container(
			name,
			stdin_open = True,
			detach = True,
			tty=True,
			#command= 'bin/sh',
		)
		#TODO cmd

		client.start(container)
		return  HttpResponse(status=200) 
	else :
		return  HttpResponse(status=404) 

def remove_image(request):
	if request.method == 'POST':

		name = json.load(request)['name']
		client = docker.from_env()
		try:
			client.images.remove(image=name)
			return  HttpResponse(status=200) 
		except docker.errors.APIError as x:
			
			response = HttpResponse(json.dumps({'err': str(x)}), 
			content_type='application/json')
			response.status_code = 409
			
			return response 
			#return HttpResponse(status=400, {'test':'plx'})
			#return HttpResponse(x, status=400)
			#return HttpResponseNotFound('<h1>Page not found</h1>')
			#print(docker.errors.APIError)


def start_stop_remove(request):
	if request.method == 'POST':
		
		json_data = json.load(request)
		cmd = json_data['cmd']
		id = json_data['id']

		client = docker.from_env()
		container = client.containers.get(id)
		if cmd == "start":
			container.start()
		elif cmd == "stop":
			container.stop()
		elif cmd == "remove":
			container.remove()
		return  HttpResponse(status=200) 


def console(request,id):
	return render(request,'console.html')


def read_and_forward_output(sid):
	# get socket object
	socket = sio.get_session(sid)['socket']
	while True:
		sio.sleep(0)
		timeout_sec = 0
		(data_ready, _, _) = select.select([socket], [], [], timeout_sec)
		if data_ready:
			output = socket._sock.recv(1024)

			# check if client disconnected
			if output == b'':
				sio.disconnect(sid)
				return 

			# decode("cp437") ; to decode vim's output
			sio.emit("pty_output", {"output": output.decode("cp437")},room=sid)

	
	   
@sio.event
def resize(sid, message): 
	client = docker.APIClient()
	#try:
	id = sio.get_session(sid)['id']
	client.resize(container=id, height=int(message["rows"]), width=int(message["cols"]))
	#except KeyError:
	#	print("session id has not been saved yet")	

@sio.event
def pty_input(sid, message):
	# get socket object 
	socket = sio.get_session(sid)['socket']
	socket._sock.send(message["input"].encode())

@sio.event
def disconnect_request(sid):
	sio.disconnect(sid)

@sio.event
def start_console(sid,message):
	client = docker.APIClient()

	# check if container is running
	if client.containers(all=True,filters={'id':message["Id"]})[0]["State"] != "running":
		sio.disconnect(sid)
		return

	socket = client.attach_socket(message["Id"], params={'stdin': 1, 'stream': 1,'stdout':1,'stderr':1})
	
	# save socket object to session	
	sio.save_session(sid, {'socket': socket,"id":message["Id"]})

	sio.start_background_task(target=read_and_forward_output(sid))


@sio.event
def connect(sid, environ):
	pass

@sio.event
def disconnect(sid):
	print('Client disconnected')


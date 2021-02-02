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
import requests

import json
from .models import *

async_mode = "eventlet"
sio = socketio.Server(async_mode=async_mode)

def index(request):
		client = docker.from_env()
		return render(request, 'index.html',{'containers':client.containers.list(all=True),'images':client.images.list(),'info':client.info()})


def browse(request):
    page_number = request.GET.get('page','1')
    q = request.GET.get('q','')

    url = 'https://hub.docker.com/api/content/v1/products/search?page='+page_number+'&page_size=15&q='+q+'&type=image'
    headers = {'Search-Version': 'v3'}

    page = requests.get(url,headers=headers)
    summary = page.json()['summaries']


    return render(request, 'browse.html', {'summary': summary,'q':q})

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
	id = sio.get_session(sid)['id']
	client.resize(container=id, height=int(message["rows"]), width=int(message["cols"]))


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
def pull_image_input(sid,message):
	client = docker.APIClient()
	try:
		x = client.pull(message["image"], stream=True,decode=True,tag=message["version"])
	except docker.errors.APIError as err:
		print("aaaa",type(err),str(err))
		sio.emit("pull_image_output", {"status": str(err), "progress": ""},room=sid)

		#uesless sleep, i just want the user to read the error message before redirection happens
		sio.sleep(3)
		sio.disconnect(sid)
		return

	for item in x:
		print("AAA",item)
		if "progress" not in item:
			item["progress"] = ""
		if "errorDetail" in item:
			item["status"] = item["errorDetail"]["message"]

		sio.emit("pull_image_output", {"status": item["status"], "progress": item["progress"]},room=sid)
		sio.sleep(0)

	sio.sleep(1.5)
	sio.disconnect(sid)


@sio.event
def connect(sid, environ):
	pass

@sio.event
def disconnect(sid):
	print('Client disconnected')


import os
from xterm.task import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound,JsonResponse
import socketio
import pty
import select
import subprocess
import struct
import fcntl
import termios 
import signal
import docker
import time
import requests

import json
from celery.result import AsyncResult

sio = socketio.Server(async_mode='eventlet')

def index(request):
		response = redirect('/containers/')
		return response
		
def containers(request):
		client = docker.from_env()
		return render(request, 'containers.html',{'containers':client.containers.list(all=True),'info':client.info()})

def images(request):
		client = docker.from_env()
		return render(request, 'images.html',{'images':client.images.list()})

# to dynamicly update the content of django template without reloading 
# TODO split front from back
def ajaxImages(request):
	client = docker.from_env()
	return render(request, 'ajaxImages.html',{'images':client.images.list()})
		
def ajaxContainers(request):
	client = docker.from_env()
	return render(request, 'ajaxContainers.html',{'containers':client.containers.list(all=True),'info':client.info()})

def console(request,id):
	client = docker.from_env()
	container = client.containers.get(id)


	return render(request,'console.html',{'id':id, 'container':container})



def browse(request):
	page_number = request.GET.get('page','1')
	q = request.GET.get('q','')

	url = 'https://hub.docker.com/api/content/v1/products/search?page='+page_number+'&page_size=15&q='+q+'&type=image'
	headers = {'Search-Version': 'v3'}

	page = requests.get(url,headers=headers)
	summary = page.json()['summaries']


	return render(request, 'browse.html', {'summary': summary,'q':q})

def runImage(request):
	if request.method == 'POST':
		name = json.load(request)['name']
		task = runImageTask.delay(name)
		return JsonResponse({"task_id":task.task_id})
	

def removeImage(request):
	if request.method == 'POST':
		name = json.load(request)['name']
		task = removeImageTask.delay(name)
		client = docker.from_env()
		return JsonResponse({"task_id":task.task_id})



def start_stop_remove(request):
	if request.method == 'POST':
		
		json_data = json.load(request)
		cmd = json_data['cmd']
		id = json_data['id']

		client = docker.from_env()
		container = client.containers.get(id)
		if cmd == "start":
			task = runContainerTask.delay(id)
		elif cmd == "stop":
			task = stopContainerTask.delay(id)
		elif cmd == "remove":
			task = removeContainerTask.delay(id)
		return JsonResponse({"task_id":task.task_id})


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

def get_progress(request, task_id):
	task = AsyncResult(task_id)
	response_data = {
		'state': task.state,
		'details': str(task.info)
	}
	return JsonResponse(response_data)
	   
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


from typing import Container
from celery import shared_task,states
from celery.utils.log import get_task_logger
import docker
from celery.exceptions import Ignore
import json


import time
logger = get_task_logger(__name__)


@shared_task()
def add (x,y):
	print("adding")

	time.sleep(1.5)
	##self.update_state(state="finished")
	
	return x+y

@shared_task()
def runImageTask(name):
	client = docker.from_env()
	container = client.containers.run(
		name,
		stdin_open = True,
		detach = True,
		tty=True,
		#command= 'bin/sh', TODO
	)
	if len(container.image.tags) == 0:
		image_name = "none"
	else:
		image_name = container.image.tags[0]

	container_name = container.attrs['Name'][1:]

	msg = f"Container {container_name} ({image_name}) has been created"

	return msg



@shared_task(bind=True)
def removeImageTask(self,name):
	client = docker.from_env()
	try:
		client.images.remove(image=name)
		msg = f"Image {name} has been removed"
		return msg
	except docker.errors.APIError as err:
		# extract error msg
		try:
			msg = str(err).split('Conflict ("')[1][:-1]  
		except:
			msg = str(err)

		self.update_state(
			state = states.FAILURE,
			meta = {
				'exc_type': "exc", 
				'exc_message': msg
				})        
		raise Ignore()


@shared_task(bind=True)
def runContainerTask(self,id):
	client = docker.from_env()
	container = client.containers.get(id)

	container.start()
	
	container_name = container.name
	msg = f"Container {container_name} has been started"

	return msg

	


@shared_task(bind=True)
def stopContainerTask(self,id):
	client = docker.from_env()
	container = client.containers.get(id)
	container.stop()
	container_name = container.name
	msg = f"Container {container_name} has been stopped"

	return msg


@shared_task(bind=True)
def removeContainerTask(self,id):
	client = docker.from_env()
	container = client.containers.get(id)
	container.remove()
	container_name = container.name
	msg = f"Container {container_name} has been removed"

	return msg

import docker, tarfile
from io import BytesIO
import time

#client = docker.APIClient()


client = docker.from_env()
#client = docker.APIClient()

container = client.containers.get("4942ad4ebc8e")

client = docker.APIClient()
#print (container.attrs["Id"])
s = client.exec_create(container.attrs["Id"],"cd bin\n",tty=True)

print(s)

print(client.exec_start(s["Id"]))
#print(client.info())
#print(s)


#print(method_list)
#print(client.containers())




#client.containers.get(container["Id"
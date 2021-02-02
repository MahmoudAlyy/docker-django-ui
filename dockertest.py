import docker

client = docker.APIClient()

#res = client.images.search("alpine")

x = client.pull("alpine:3.11", stream=True,decode=True)

for item in x:
	print(item)

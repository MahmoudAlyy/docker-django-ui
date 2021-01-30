from django.db import models
from django.contrib.auth.models import User

class Docker(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="docker")
	instance_id = models.TextField()
	instance_name = models.TextField()

	def __str__(self):
		return f"{self.instance_name|self.instance_id[0:5]}"

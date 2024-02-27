from django.db import models

class User(models.Model):
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	username = models.CharField(max_length=250)
	email = models.EmailField(max_length=150)
	password = models.CharField(max_length=250)

	def __str__(self):
		return self.firstname + ' ' + self.lastname + ' - ' + self.username
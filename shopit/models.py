from django.db import models

class User(models.Model):
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	username = models.CharField(max_length=250)
	email = models.EmailField(max_length=150)
	password = models.CharField(max_length=250)

	def __str__(self):
		return self.firstname + ' ' + self.lastname + ' - ' + self.username

class Product(models.Model):
	productname = models.CharField(max_length=100)
	productdescription = models.TextField(null=True, blank=True)
	productprice = models.DecimalField(max_digits=12, decimal_places=2)
	productimage = models.ImageField(upload_to='products/')

	def __str__(self):
		return self.productname + ' ' + str(self.productprice)
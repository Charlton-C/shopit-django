from django.db import models

class Product(models.Model):
	productname = models.CharField(max_length=100)
	productdescription = models.TextField(null=True, blank=True)
	productprice = models.DecimalField(max_digits=12, decimal_places=2)
	productimage = models.ImageField(upload_to='products/')

	def __str__(self):
		return self.productname + ' ' + str(self.productprice)
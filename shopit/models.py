from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	productname = models.CharField(max_length=100)
	productdescription = models.TextField(null=True, blank=True)
	productprice = models.DecimalField(max_digits=12, decimal_places=2)
	productimage = models.ImageField(upload_to='products/')

	def __str__(self):
		return self.productname + ' - ' + str(self.productprice)

class Cart(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	data_added = models.DateTimeField(auto_now_add=True)

	def itemTotalCost(self):
		return self.product.productprice * self.quantity

	def __str__(self):
		return str(self.quantity) + ' - ' + self.product.productname + ' - added by ' + self.user.first_name + ' ' + self.user.last_name + ' (' + self.user.username + ')'
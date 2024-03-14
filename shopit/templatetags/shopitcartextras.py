from django import template
from shopit.models import Cart

register = template.Library()

@register.filter(name="productExistsInUserCart")
def productExistsInUserCart(user, product):
	if Cart.objects.filter(product=product, user=user).exists():
		return Cart.objects.get(product=product, user=user).quantity
	else:
		return None

register.filter("productExistsInUserCart", productExistsInUserCart)
from django import template
from shopit.models import Cart

register = template.Library()

@register.filter(name="productExistsInCart")
def productExistsInCart(product):
	if Cart.objects.filter(product=product).exists():
		return Cart.objects.get(product=product).quantity
	else:
		return None

register.filter("productExistsInCart", productExistsInCart)
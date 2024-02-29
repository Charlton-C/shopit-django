from django.urls import path
from shopit import views

urlpatterns = [
	path('signup/', views.signUpUser, name='signUpUser'),
	path('login/', views.logInUser, name='logInUser'),
	path('home/', views.home, name='home'),
	path('products/', views.products, name='products'),
	path('cart/', views.usercart, name='cart'),
	path('addtocart/h/<int:productID>/', views.addToCartFromHome, name='addToCartFromHome'),
	path('addtocart/p/<int:productID>/', views.addToCartFromProducts, name='addToCartFromProducts'),
	path('removefromcart/<int:itemID>/', views.removeFromCart, name='removeFromCart'),
]
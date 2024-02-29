from django.urls import path
from shopit import views

urlpatterns = [
	path('signup/', views.signUpUser, name='signUpUser'),
	path('login/', views.logInUser, name='logInUser'),
	path('logout/', views.logOutUser, name='logOutUser'),
	path('home/', views.home, name='home'),
	path('products/', views.products, name='products'),
	path('cart/', views.usercart, name='cart'),
	path('profile/', views.userprofile, name='profile'),
]
from django.urls import path
from shopit import views

urlpatterns = [
	path('signup/', views.signUpUser, name='signUpUser'),
	path('login/', views.logInUser, name='logInUser'),
	path('home/', views.home, name='home'),
]
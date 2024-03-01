from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from shopit.models import Product


def home(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		return render(request, 'home.html')

def products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})

def usercart(request):
	return render(request, 'usercart.html')

def userprofile(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		return render(request, 'userprofile.html', {'user': request.user})

def updateUserProfile(request):
	if request.method == "POST":
		user = request.user
		user.first_name = request.POST['userfirstname']
		user.last_name = request.POST['userlastname']
		user.email = request.POST['useremail']
		user.save()
		return render(request, 'userprofile.html', {'user': request.user})


def signUpUser(request):
	if request.method == "POST":
		if request.POST['password'] == request.POST['confirmpassword']:
			user = User.objects.create_user(request.POST['username'], first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], password=request.POST['password'])
			login(request, user)
			return redirect('home')
		else:
			return render(request, 'signup.html', {'firstname': request.POST['firstname'], 'lastname': request.POST['lastname'], 'username': request.POST['username'], 'email': request.POST['email'], 'confirmpasswordErrorMessage': 'Passwords don\'t match'})
	else:
		return render(request, 'signup.html', {'confirmpasswordErrorMessage': ''})
	

def logInUser(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(reverse('home'))
		else:
			return render(request, 'login.html', {'username': request.POST['username']})
	else:
		return render(request, 'login.html', {'username': ''})

def logOutUser(request):
	logout(request)
	return redirect('logInUser')

def deleteUserAccount(request):
	user = request.user
	logout(request)
	user.delete()
	return redirect('signUpUser')
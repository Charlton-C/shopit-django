from django.shortcuts import render, redirect
from django.urls import reverse
from shopit.models import Product
from shopit.forms import UserForm


def home(request):
	return render(request, 'home.html')

def products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})


def signUpUser(request):
	if request.method == "POST":
		if request.POST['password'] == request.POST['confirmpassword']:
			form = UserForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect(reverse('home'))
			else:
				return render(request, 'signup.html', {'firstname': request.POST['firstname'], 'lastname': request.POST['lastname'], 'username': request.POST['username'], 'email': request.POST['email']})
		else:
			return render(request, 'signup.html', {'firstname': request.POST['firstname'], 'lastname': request.POST['lastname'], 'username': request.POST['username'], 'email': request.POST['email']})

	else:
		return render(request, 'signup.html')
	

def logInUser(request):
	if request.method == "POST":
		user = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])
		try:
			if user[0] == None:
				raise
			else:
				return redirect(reverse('home'))
		except:
			return render(request, 'login.html', {'email': request.POST['email']})
	else:
		return render(request, 'login.html')
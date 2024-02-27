from django.shortcuts import render, redirect
from django.urls import reverse
from shopit.forms import UserForm

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
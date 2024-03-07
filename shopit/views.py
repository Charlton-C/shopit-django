import time
from django.shortcuts import render, redirect
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from shopit.models import Product, Cart


def home(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		products = Product.objects.all().order_by('-id')[:5]
		return render(request, 'home.html', {'products': products})


def products(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		products = Product.objects.all()
		return render(request, 'products.html', {'products': products})


def usercart(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		cartItems = Cart.objects.filter(user=request.user)
		totalpriceforallcartitem = sum(cartItem.product.productprice * cartItem.quantity for cartItem in cartItems)
		return render(request, 'usercart.html', {'cartitems': cartItems, 'totalpriceforallcartitem': totalpriceforallcartitem})

def addToCartFromHome(request, productID):
	product = Product.objects.get(id=productID)
	cartItem, created = Cart.objects.get_or_create(product=product, user=request.user)
	cartItem.quantity += 1
	cartItem.save()
	return redirect('home')

def addToCartFromProducts(request, productID):
	product = Product.objects.get(id=productID)
	cartItem, created = Cart.objects.get_or_create(product=product, user=request.user)
	cartItem.quantity += 1
	cartItem.save()
	return redirect('products')

def removeFromCart(request, itemID):
	cartItem = Cart.objects.get(id=itemID)
	if cartItem.quantity == 1:
		cartItem.delete()
	else:
		cartItem.quantity -= 1
		cartItem.save()
	return redirect('cart')

def buyAllItems(request, totalcostofallitems):
	if request.method == "POST":
		if len(request.POST['numbermakingpayment']) >= 9:
			paymenterrormessage = ''
			paymentsuccessmessage = ''
			mc = MpesaClient()
			number = request.POST['numbermakingpayment']
			if number[0] == '0':
				number = '254' + number[1:]
			elif number[0] == '+':
				number = number[1:]
			elif number[0] == '7':
				number = '254' + number
			else:
				None
			amount = int(totalcostofallitems)
			account_reference = 'reference'
			transaction_description = 'test payment'
			callback_url = 'https://api.darajambili.com/express-payment'
			print(mc.stk_push(number, amount, account_reference, transaction_description, callback_url))
			if False:
				cartItems = Cart.objects.filter(user=request.user)
				for cartItem in cartItems:
					cartItem.delete()
				cartItems = Cart.objects.filter(user=request.user)
				paymentsuccessmessage = 'Payment successful!'
				return render(request, 'usercart.html', {'cartitems': cartItems, 'paymentsuccessmessage': paymentsuccessmessage})
			elif True:
				time.sleep(8)
				cartItems = Cart.objects.filter(user=request.user)
				totalpriceforallcartitem = sum(cartItem.product.productprice * cartItem.quantity for cartItem in cartItems)
				paymenterrormessage = 'Payment not successful, please try again'
				return render(request, 'usercart.html', {'cartitems': cartItems, 'totalpriceforallcartitem': totalpriceforallcartitem, 'paymenterrormessage': paymenterrormessage})
			else:
				None
		elif len(request.POST['numbermakingpayment']) < 9:
			cartItems = Cart.objects.filter(user=request.user)
			totalpriceforallcartitem = sum(cartItem.product.productprice * cartItem.quantity for cartItem in cartItems)
			paymenterrormessage = 'Please enter a valid number'
			return render(request, 'usercart.html', {'cartitems': cartItems, 'totalpriceforallcartitem': totalpriceforallcartitem, 'paymenterrormessage': paymenterrormessage})
		else:
			cartItems = Cart.objects.filter(user=request.user)
			totalpriceforallcartitem = sum(cartItem.product.productprice * cartItem.quantity for cartItem in cartItems)
			paymenterrormessage = 'Something went wrong'
			return render(request, 'usercart.html', {'cartitems': cartItems, 'totalpriceforallcartitem': totalpriceforallcartitem, 'paymenterrormessage': paymenterrormessage})


def userprofile(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		return render(request, 'userprofile.html', {'user': request.user})

def updateUserProfile(request):
	if request.method == "POST":
		errorMessage = ''
		successMessage = ''
		user = request.user
		user.first_name = request.POST['userfirstname']
		user.last_name = request.POST['userlastname']
		user.email = request.POST['useremail']
		user.save()
		successMessage = 'Profile updated'
		# Update username
		if request.POST['username'] == user.username:
			None
		elif request.POST['username'] != user.username and User.objects.filter(username=request.POST['username']).exists():
			errorMessage = 'Username is already taken'
		elif request.POST['username'] != user.username and User.objects.filter(username=request.POST['username']).exists() == False:
			user.username = request.POST['username']
			user.save()
			successMessage = 'Profile updated'
		else:
			errorMessage = 'Something went wrong with saving your username'
		# Update password
		if request.POST['oldpassword'] == '':
			None
		elif request.POST['oldpassword'] != '' and check_password(request.POST['oldpassword'], user.password) == False:
			if errorMessage != '':
				errorMessage += '\nYour old password is wrong'
			elif errorMessage == '':
				errorMessage = 'Your old password is wrong'
			else:
				None
		elif request.POST['oldpassword'] != '' and check_password(request.POST['oldpassword'], user.password):
			user.set_password(request.POST['password'])
			user.save()
			successMessage = 'Profile updated'
		else:
			if errorMessage != '':
				errorMessage += '\nSomething went wrong with saving your password'
			elif errorMessage == '':
				errorMessage = 'Something went wrong with saving your password'
			else:
				None
		# Remove success message if their is an error
		if errorMessage != '':
			successMessage = ''
		return render(request, 'userprofile.html', {'user': request.user, 'passwordSaveErrorMessage': errorMessage, 'passwordSaveSuccessMessage': successMessage})


def signUpUser(request):
	if request.method == "POST":
		if User.objects.filter(username=request.POST['username']).exists():
			return render(request, 'signup.html', {'firstname': request.POST['firstname'], 'lastname': request.POST['lastname'], 'username': '', 'email': request.POST['email'], 'signuperrormessage': 'User already exists'})
		if request.POST['password'] == request.POST['confirmpassword']:
			user = User.objects.create_user(request.POST['username'], first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], password=request.POST['password'])
			login(request, user)
			return redirect('home')
		else:
			return render(request, 'signup.html', {'firstname': request.POST['firstname'], 'lastname': request.POST['lastname'], 'username': request.POST['username'], 'email': request.POST['email'], 'signuperrormessage': 'Passwords don\'t match'})
	else:
		return render(request, 'signup.html')


def logInUser(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		if User.objects.filter(username=username).exists():
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				return render(request, 'login.html', {'username': request.POST['username'], 'loginerrormessage': 'Please check your password and try again'})
		else:
			return render(request, 'login.html', {'username': '', 'loginerrormessage': 'The user does not exist'})
	else:
		return render(request, 'login.html')

def logOutUser(request):
	logout(request)
	return redirect('logInUser')

def deleteUserAccount(request):
	user = request.user
	logout(request)
	user.delete()
	return redirect('signUpUser')
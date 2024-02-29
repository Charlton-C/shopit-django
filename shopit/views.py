from django.shortcuts import render, redirect
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from shopit.models import Product, Cart


def home(request):
	if not request.user.is_authenticated:
		return logInUser(request)
	else:
		return render(request, 'home.html')

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
	return render(request, 'home.html')
	
def addToCartFromProducts(request, productID):
	product = Product.objects.get(id=productID)
	cartItem, created = Cart.objects.get_or_create(product=product, user=request.user)
	cartItem.quantity += 1
	cartItem.save()
	return render(request, 'products.html', {'products':  Product.objects.all()})

def removeFromCart(request, itemID):
	cartItem = Cart.objects.get(id=itemID)
	if cartItem.quantity == 1:
		cartItem.delete()
	else:
		cartItem.quantity -= 1
		cartItem.save()
	cartItems = Cart.objects.filter(user=request.user)
	totalpriceforallcartitem = sum(cartItem.product.productprice * cartItem.quantity for cartItem in cartItems)
	return render(request, 'usercart.html', {'cartitems': cartItems, 'totalpriceforallcartitem': totalpriceforallcartitem})

def buyAllItems(request, totalcostofallitems):
	if request.method == "POST":
		mc = MpesaClient()
		number = request.POST['numbermakingpayment']
		amount = int(totalcostofallitems)
		account_reference = 'reference'
		transaction_description = 'test payment'
		callback_url = 'https://api.darajambili.com/express-payment'
		print(mc.stk_push(number, amount, account_reference, transaction_description, callback_url))
		cartItems = Cart.objects.filter(user=request.user)
		for cartItem in cartItems:
			cartItem.delete()
		cartItems = Cart.objects.filter(user=request.user)
		return render(request, 'usercart.html', {'cartitems': cartItems, 'totalpriceforallcartitem': '0'})

def signUpUser(request):
	if request.method == "POST":
		if request.POST['password'] == request.POST['confirmpassword']:
			User.objects.create_user(request.POST['username'], first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'], password=request.POST['password'])
			return redirect(reverse('home'))
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
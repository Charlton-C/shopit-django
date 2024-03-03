from django.urls import path
from shopit import views

urlpatterns = [
	path('signup/', views.signUpUser, name='signUpUser'),
	path('login/', views.logInUser, name='logInUser'),
	path('logout/', views.logOutUser, name='logOutUser'),
	path('deleteaccount/', views.deleteUserAccount, name='deleteUserAccount'),
	path('profile/', views.userprofile, name='profile'),
	path('updateuserprofile/', views.updateUserProfile, name='updateUserProfile'),
	path('home/', views.home, name='home'),
	path('products/', views.products, name='products'),
	path('cart/', views.usercart, name='cart'),
	path('addtocart/h/<int:productID>/', views.addToCartFromHome, name='addToCartFromHome'),
	path('addtocart/p/<int:productID>/', views.addToCartFromProducts, name='addToCartFromProducts'),
	path('removefromcart/<int:itemID>/', views.removeFromCart, name='removeFromCart'),
	path('buyallitems/<int:totalcostofallitems>/', views.buyAllItems, name='buyAllItems'),
]
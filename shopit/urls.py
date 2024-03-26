from django.urls import path
from shopit import views

urlpatterns = [
	path('signup/', views.signUpUser, name='signUpUser'),
	path('login/', views.logInUser, name='logInUser'),
	path('logout/', views.logOutUser, name='logOutUser'),
	path('deleteaccount/', views.deleteUserAccount, name='deleteUserAccount'),
	path('accountdeleted/', views.userAccountDeleted, name='userAccountDeleted'),
	path('profile/', views.userprofile, name='profile'),
	path('updateuserprofile/', views.updateUserProfile, name='updateUserProfile'),
	path('home/', views.home, name='home'),
	path('products/', views.products, name='products'),
	path('cart/', views.usercart, name='cart'),
	path('addtocart/h/<int:productID>/', views.addToCartFromHome, name='addToCartFromHome'),
	path('addtocart/p/<int:productID>/', views.addToCartFromProducts, name='addToCartFromProducts'),
	path('removefromcart/h/<int:productID>/', views.removeItemFromCartFromHomePage, name='removeItemFromCartFromHomePage'),
	path('removefromcart/p/<int:productID>/', views.removeItemFromCartFromProductsPage, name='removeItemFromCartFromProductsPage'),
	path('removefromcart/c/<int:itemID>/', views.removeItemFromCartFromCartPage, name='removeItemFromCartFromCartPage'),
	path('buyallitems/<int:totalcostofallitems>/', views.buyAllItems, name='buyAllItems'),
]
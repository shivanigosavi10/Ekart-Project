"""
URL configuration for Ekart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  ecomapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('register/', views.register),
     path('login/', views.user_login),
     path('base/', views.hello),
     path('home/', views.home),
     path('product_details/<pid>', views.pdetails),
     path('about/', views.about),
     path('contact/', views.contact),
     path('user_logout/', views.user_logout),
     path('product/', views.product),
     path('catfilter/<cv>', views.catfilter),
     path("sort/<sv>", views.sortprice),
     path("filterbyprice", views.filterbyprice),
    #  path('cartV/', views.viewcart),
     path('cart/<pid>', views.cart),
     path('view_cart', views.viewcart),
     path('remove/<cid>', views.remove),
     path('updateqty/<x>/<cid>', views.updateqty),
     path('placeorder/', views.placeorder),
     path('fetchorder/', views.fetchorder),
     path('makepay', views.makepayment),
     path('paymentsuccess/', views.paymentsuccess),
     path('add_address',views.createAddress , name='add_address'),
     path('infodata/',views.infodata)
    #  path('change_pass/<token>/', views.ChangePassword),
    #  path('forgot_password/', views.forgot_password),
     
]


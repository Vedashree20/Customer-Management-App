from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logoutuser, name= 'logout'),
    path('products/', views.products, name='Products'),
    path('customer/<str:pk_test>/', views.customers, name='Customers'),
    path('createorder/<str:pk>/',views.createOrder,name='createorder'),
    path('updateorder/<str:pk>/',views.updateOrder, name='updateorder'),
    path('deleteorder/<str:pk>/',views.deleteOrder, name='deleteorder'),
    path('login/',views.loginpage, name='login'),
    path('user/',views.userPage, name='user-page'),
    path('register/',views.registerpage, name='register'),
    path('account/', views.accountSettings, name='account')
]

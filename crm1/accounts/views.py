import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import Orderfilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_users,admin_only

# Create your views here.

@unauthenticated_user
def loginpage(request):

    if request.method == 'POST':
            username =   request.POST.get('username')
            password =   request.POST.get('password')

            user = authenticate(request, username=username, password=password)
    
            if user is not None:
                login(request,user)
                return redirect('home')

            else:
                messages.info(request, 'Username or password is incorrect')
   
    context={}
    return render(request,'accounts/login.html')

    
def logoutuser(request):

    logout(request)
    return redirect('login')

@unauthenticated_user
def registerpage(request):

    if request.user.is_authenticated:
        return redirect('home')

    else:    
        form=UserCreationForm()

        if request.method == 'POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username= form.cleaned_data.get('username')
                # group=Group.objects.get(name="Customers")
                # user.groups.add(group)
                # customer.objects.create(
				#     user=user,
				#     name=user.username,
				# )#simultaneouos account creation along with user
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)    


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def userPage(request):

    orders=request.user.customer.order_set.all()

    print("ORDERS: ", orders)
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
  

    context={'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}

    return render(request,'accounts/user.html',context)

@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=customer.objects.all()
    total_customers=customers.count()

    delivered=orders.filter(status='Delivered').count()

    pending=orders.filter(status='Pending').count()

    total_orders=orders.count()

    context={'orders':orders,'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}

    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request, 'accounts/accounts_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{"products":products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customers(request, pk_test):
    Customer = customer.objects.get(id=pk_test)
    orders=Customer.order_set.all()

    order_count = orders.count()

    myFilter = Orderfilter(request.GET, queryset=orders)
    orders=myFilter.qs

    context = {'customer':Customer,'orders':orders,'order_count':order_count,'myfilter':myFilter}
    return render(request,'accounts/customer.html',context)

@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(customer, Order, fields=('product', 'status'))    
    Customer= customer.objects.get(id=pk)
    formset = OrderFormSet(instance=Customer)
    #form=OrderForm(initial={'customer': Customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        formset= OrderFormSet(request.POST,instance=Customer)
        #if formset.is_valid():
        formset.save()#handled by the model form
        return redirect('/')
        
    context={'formset': formset}    
    return render(request, 'accounts/order_form.html', context)

@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def deleteOrder(request, pk):
    
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)


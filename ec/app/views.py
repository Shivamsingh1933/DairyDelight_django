from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer, Cart
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.
def home(request):
    return render(request, "app/home.html")

def contact(request):
    return render(request, "app/contact.html")

def about(request):
    return render(request, "app/about.html")



class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request, "app/category.html", locals())
    
    

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form  = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            
        else:
            messages.warning(request, "Registration Failed")
        return render(request, "app/customerregistration.html", locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            zipcode = form.cleaned_data["zipcode"]
            state = form.cleaned_data["state"]
            
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, zipcode=zipcode, state=state)
            reg.save()
            messages.success(request, "congratulation! Profile Save successfully")
            
        else:
            messages.warning(request, "Profile Failed")
        return render(request, "app/profile.html", locals())
          
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", locals())


class updateAddressView(View): 
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance = add)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data["name"]
            add.locality = form.cleaned_data["locality"]
            add.city = form.cleaned_data["city"]
            add.mobile = form.cleaned_data["mobile"]
            add.zipcode = form.cleaned_data["zipcode"]
            add.state = form.cleaned_data["state"]
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
            
        else:
            messages.warning(request, "Profile Updation Failed")
        return redirect("address")
            
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40  
    return render(request, 'app/addtocart.html',locals())


class checkout(View):
    def get(self, request):
        user=request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount = famount + value
        totalamount=famount+40
        return render(request, 'app/checkout.html', locals())
        







def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save() 
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        
        data = {
            'quantity': c.quantity,
            'totalamount': totalamount,
            'amount': amount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save() 
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        
        data = {
            'quantity': c.quantity,
            'totalamount': totalamount,
            'amount': amount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0
        for p in cart:
            value = p.quantity*p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        
        data = {
            'totalamount': totalamount,
            'amount': amount
        }
        return JsonResponse(data)
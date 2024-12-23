from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer, Cart, OrderPlaced, Payment, Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import razorpay 
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import razorpay
from .models import Customer, Cart, Payment
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
import razorpay
from django.conf import settings
from .models import Customer, Cart, Payment, OrderPlaced
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from reportlab.pdfgen import canvas
from .models import Payment, OrderPlaced, Customer, Cart


@login_required
# Create your views here.
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())


@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())



class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category = product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
        
        return render(request, "app/category.html", locals())
    
    

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product)& Q(user=request.user))
        
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", locals())
    
    
class CustomerRegistrationView(View):
    def get(self, request):
        form  = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
        return render(request, "app/customerregistration.html", locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            
        else:
            messages.warning(request, "Registration Failed")
        return render(request, "app/customerregistration.html", locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
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
            email = form.cleaned_data["email"]
            
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, zipcode=zipcode, state=state, email=email)
            reg.save()
            messages.success(request, "congratulation! Profile Save successfully")
            
        else:
            messages.warning(request, "Profile Failed")
        return render(request, "app/profile.html", locals())
          
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
   
    return render(request, "app/address.html", locals())


class updateAddressView(View): 
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance = add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
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
            add.email = form.cleaned_data["email"]
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
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
        
    return render(request, 'app/addtocart.html',locals())


@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        #{'amount': 50800, 'amount_due': 50800, 'amount_paid': 0, 'attempts': 0, 'created_at': 1734561741, 'currency': 'INR', 'entity': 'order', 'id': 'order_PYo9O6JIyCSSBz', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                razorpay_order_id=order_id,
                amount=totalamount,
                razorpay_payment_status=order_status
            )
            
            payment.save()
        return render(request, 'app/checkout.html', locals())






def payment_done(request):
    # Fetching data from GET parameters
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')  # Selected address ID

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))  # Redirect to login page if not authenticated

    try:
        # Get the customer using the logged-in user and selected customer ID
        user = request.user
        customer = Customer.objects.get(user=user, id=cust_id)  # Use cust_id to select the correct address

        # Fetch the payment details using the order_id
        payment = Payment.objects.get(razorpay_order_id=order_id)

        # Update the payment details with the received payment_id and mark as paid
        payment.razorpay_payment_id = payment_id
        payment.paid = True
        payment.save()

        # Now, update the cart and create an order
        cart = Cart.objects.filter(user=user)  # Get the cart items for the authenticated user
        for c in cart:
            # Create the order and associate it with the selected customer
            OrderPlaced(user=user, customer=customer, payment=payment, product=c.product, quantity=c.quantity).save()
            c.delete()  # Clear the cart item after placing the order

        return render(request, 'app/paymentdone.html', locals())

    except Customer.DoesNotExist:
        return HttpResponse("Invalid customer ID", status=404)
    except Payment.DoesNotExist:
        return HttpResponse("Invalid payment details", status=404)



     








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
            'amount': amount,
            'is_empty': cart.count() == 0,
        }
        return JsonResponse(data)
    



def payment_done(request):
    # Fetching data from GET parameters
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')  # Selected address ID

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    try:
        user = request.user
        customer = Customer.objects.get(user=user, id=cust_id)
        payment = Payment.objects.get(razorpay_order_id=order_id)

        # Update payment details
        payment.razorpay_payment_id = payment_id
        payment.paid = True
        payment.save()

        # Process cart and create orders
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(
                user=user,
                customer=customer,
                payment=payment,
                product=c.product,
                quantity=c.quantity
            ).save()
            c.delete()

        return render(request, 'app/paymentdone.html', {'payment': payment})

    except Customer.DoesNotExist:
        return HttpResponse("Invalid customer ID", status=404)
    except Payment.DoesNotExist:
        return HttpResponse("Invalid payment details", status=404)


def download_receipt(request, payment_id):
    try:
        # Fetch payment and related orders
        payment = Payment.objects.get(razorpay_payment_id=payment_id)
        orders = OrderPlaced.objects.filter(payment=payment)

        # Generate PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{payment_id}.pdf"'

        pdf = canvas.Canvas(response)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, 800, "Payment Receipt")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 770, f"Transaction ID: {payment.razorpay_payment_id}")
        pdf.drawString(100, 750, f"Order ID: {payment.razorpay_order_id}")
        pdf.drawString(100, 730, f"Amount Paid: Rs. {payment.amount}")
        pdf.drawString(100, 710, f"Payment Status: {'Paid' if payment.paid else 'Pending'}")
        pdf.drawString(100, 690, f"Customer: {payment.user.username}")

        y = 670
        for order in orders:
            pdf.drawString(100, y, f"Product: {order.product.title} (Quantity: {order.quantity})")
            y -= 20

        pdf.drawString(100, y - 20, "Thank you for your purchase!")
        pdf.showPage()
        pdf.save()

        return response
    except Payment.DoesNotExist:
        return HttpResponse("Payment details not found", status=404)


@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed= OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


@login_required
def plus_wishlist(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data={
        'message': 'Wishlist Added Successfully',
        }

        return JsonResponse(data)
    
    
@login_required
def minus_wishlist(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data={
        'message': 'Wishlist removed Successfully',
        }

        return JsonResponse(data)
    
@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", locals())


@login_required
def show_wishlist(request):
    user=request.user
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, "app/wishlist.html", locals())
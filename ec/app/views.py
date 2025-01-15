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
from django.contrib.auth import authenticate, login



# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())


def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())



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

        # Check if the user is authenticated
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        else:
            wishlist = None
            totalitem = 0
            wishitem = 0
        
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



from django.shortcuts import redirect


class checkout(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        
        # Proceed with the rest of the logic after ensuring the user is authenticated
        totalitem = 0
        wishitem = 0
        totalamount = 0
        razoramount = 0

        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value

        totalamount = famount + 40
        razoramount = int(totalamount * 100)

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)

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
    


@login_required
def payment_done(request):
    # Print session info before anything else
    print(f"Session before payment: {request.session.session_key}")
    print(f"User authenticated: {request.user.is_authenticated}")
    
    if not request.user.is_authenticated:
        print("User is not authenticated. Redirecting to login.")
        return redirect('login')  # Explicit redirect to the login page if the user is not authenticated
    
    # Continue with your logic
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
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

        print(f"Session after payment: {request.session.session_key}")
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
        prod_id = request.GET.get('prod_id')
        try:
            product = Product.objects.get(id=prod_id)
            Wishlist.objects.get_or_create(user=request.user, product=product)
            data = {
                'message': 'Wishlist Added Successfully',
            }
        except Product.DoesNotExist:
            data = {
                'message': 'Product does not exist',
            }
        return JsonResponse(data)
    
@login_required
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        try:
            product = Product.objects.get(id=prod_id)
            Wishlist.objects.filter(user=request.user, product=product).delete()
            data = {
                'message': 'Wishlist removed Successfully',
            }
        except Product.DoesNotExist:
            data = {
                'message': 'Product does not exist',
            }
        return JsonResponse(data)
    

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


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
import json

@csrf_exempt
def razorpay_webhook(request):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    # Read the request body
    payload = request.body
    signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')

    # Verify the webhook signature
    try:
        client.utility.verify_webhook_signature(payload, signature, settings.RAZORPAY_WEBHOOK_SECRET)
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Parse the payload data
    event = json.loads(payload)

    # Handle the payment success event
    if event['event'] == 'payment.captured':
        payment_id = event['payload']['payment']['entity']['id']
        order_id = event['payload']['payment']['entity']['order_id']

        payment = Payment.objects.get(razorpay_order_id=order_id)
        payment.razorpay_payment_id = payment_id
        payment.paid = True
        payment.save()

        # Process cart and create orders
        cart = Cart.objects.filter(user=payment.user)
        for c in cart:
            OrderPlaced(
                user=payment.user,
                customer=c.user.customer,
                payment=payment,
                product=c.product,
                quantity=c.quantity
            ).save()
            c.delete()

    return JsonResponse({'status': 'success'}, status=200)
'''
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
'''
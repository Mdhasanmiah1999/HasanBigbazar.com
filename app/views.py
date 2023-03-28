from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, BuyOrder, Order
from .forms import CustomerRegistrationForm, CustomerProfileForm, PaymentMethodForm
from .forms import AuthenticationForm
from django.contrib import messages
from .forms import forms as LoginForm
from django.db import models as Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.db.models import Q
import pyotp
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate  
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from .models import Transaction
from .sslcommerz import sslcommerz_payment_gateway

#from sslcommerz_python.payment import SSLCSession
from decimal import Decimal




from app import forms


class ProductView(View):
 def get(self, request):
    totalitem = 0
    topwears = Product.objects.filter(category='TW')
    bottomwears = Product.objects.filter(category='BW')
    mobiles = Product.objects.filter(category='M')
    laptop = Product.objects.filter(category='L')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/home.html',{'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptop': laptop, 'totalitem': totalitem})


def mobile(request, data=None):
 if data == None:
     mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
     mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)    
 return render(request, 'app/mobile.html', {'mobiles':mobiles})


def laptop(request, data=None):
 if data == None:
     laptop = Product.objects.filter(category='L')
 elif data == 'hp' or data == 'samsung':
     laptop = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
     laptop = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
 elif data == 'above':
     laptop = Product.objects.filter(category='L').filter(discounted_price__gt=40000)    
 return render(request, 'app/laptop.html', {'laptop':laptop})

 
def topwear(request, data=None):
 if data == None:
     topwears = Product.objects.filter(category='Tw')
 elif data == 'zara' or data == 'lotto':
     topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
     topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
 elif data == 'above':
     topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)    
 return render(request, 'app/topwear.html', {'topwears':topwears})



def bottomwear(request, data=None):
 if data == None:
     bottomwears = Product.objects.filter(category='BW')
 elif data == 'zara' or data == 'lotto':
     bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
 elif data == 'above':
     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)    
 return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})

    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = True
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart})

def SearchProduct(request):
        query = request.GET.get('query')
        product = Product.objects.filter(title__icontains=query)
            
        return render(request, 'app/search.html', {'product': product})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    


def login(request):
    form = AuthenticationForm()
    return render(request, 'app/login.html', {'form':form})

def fairebase_login(request):
    form = AuthenticationForm()
    return render(request, 'fairebase_login.html')

def login_firebase(request):
    return render(request,"login_firebase.html")


@method_decorator(login_required, name='dispatch')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user 
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']    
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'congratulations! profile udated successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})



@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def buy_now(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    BuyOrder(user=user, product=product).save()
    if request.user.is_authenticated:
        user = request.user
        buy = BuyOrder.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0
        cart_product = [p for p in BuyOrder.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += int(tempamount)
                total_amount = amount + shipping_amount
        return render(request, 'app/buynow.html', {'buy':buy, 'total_amount':total_amount, 'amount':amount})


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += int(tempamount)
                total_amount = amount + shipping_amount
        return render(request, 'app/addtocart.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
    else:
        return render(request, 'app/emptycart.html')






def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        user = request.user
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        
        for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += int(tempamount)
                total_amount = amount + shipping_amount
                
                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'total_amount': total_amount
                }
        return JsonResponse(data)
    
    
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        user = request.user
        c.quantity +=-1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        
        for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += int(tempamount)
                total_amount = amount + shipping_amount
                
                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'total_amount': total_amount
                }
        return JsonResponse(data)        
     



@login_required
def checkout(request):  
    user = request.user
    add = Customer.objects.filter(user=user)
    payment_method = PaymentMethodForm()
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        
        for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
    
    return render(request, 'app/checkout.html', {'add':add, 'total_amount':total_amount, 'cart_items':cart_items})  


def checkout1(request):  
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = BuyOrder.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in BuyOrder.objects.all() if p.user == user]
    if cart_product:
        
        for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
    
    return render(request, 'app/checkout1.html', {'add':add, 'total_amount':total_amount, 'cart_items':cart_items})  


@login_required
def payment_done(request):
   
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    
    for c in cart:
      OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
    return redirect("orders")



from django.shortcuts import render  
from django.http import HttpResponse  
  
def setcookie(request):  
    response = HttpResponse("Cookie Set")  
    response.set_cookie('java-tutorial', 'javatpoint.com')  
    return response  
def getcookie(request):  
    tutorial  = request.COOKIES['java-tutorial']  
    return HttpResponse("java tutorials @: "+  tutorial);  
def test_cookie(request):   
    if not request.COOKIES.get('team'):
        response = HttpResponse("Visiting for the first time.")
        response.set_cookie('team', 'barcelona')
        return response
    else:
        return HttpResponse("Your favorite team is {}".format(request.COOKIES['team']))


def DonateView(request):
    #user = request.POST['user']
    name = request.POST.get('name', None)
    #amount = request.POST['amount']
    amount = request.POST.get('amount', None)
    return redirect(sslcommerz_payment_gateway(request, name, amount))

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutSuccessView(View):
    model = Transaction
    template_name = 'app/checkout.html'

    
    def get(self, request, *args, **kwargs):

        # return render(request, self.template_name,{'transaction':transaction})
       return render(request, 'app/checkout.html')
   
    def post(self, request, *args, **kwargs):

        data = self.request.POST

        # user = get_object_or_404(CustomUser, id=data['value_a']) #value_a is a user instance
        # cart = get_object_or_404(Cart, id = data['value_b'] ) #value_b is a user cart instance
        
        try:
            Transaction.objects.create(
                user = data['value_a'],
                tran_id=data['tran_id'],
                val_id=data['val_id'],
                amount=data['amount'],
                card_type=data['card_type'],
                card_no=data['card_no'],
                store_amount=data['store_amount'],
                bank_tran_id=data['bank_tran_id'],
                status=data['status'],
                tran_date=data['tran_date'],
                currency=data['currency'],
                card_issuer=data['card_issuer'],
                card_brand=data['card_brand'],
                card_issuer_country=data['card_issuer_country'],
                card_issuer_country_code=data['card_issuer_country_code'],
                verify_sign=data['verify_sign'],
                verify_sign_sha2=data['verify_sign_sha2'],
                currency_rate=data['currency_rate'],
                risk_title=data['risk_title'],
                risk_level=data['risk_level'],

            )
            messages.success(request,'Payment Successfull')

        except:
            messages.success(request,'Something Went Wrong')
        return render(request, 'app/success.html')


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutFaildView(View):
    template_name = 'app/faild.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    

    
    
    
        #return HttpResponse('This is a search')
    
        
        
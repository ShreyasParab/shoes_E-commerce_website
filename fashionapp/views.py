from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from fashionapp.forms import CustomerRegistrationForm, CustomerProfileForm
from fashionapp.models import Product, Customer, Cart, OrderPlaced


# Create your views here.
def home(request):
    return render(request,'home.html')

class ProdutView(View):
 def get(self, request):
  totalitem = 0
  shoes = Product.objects.filter(category='S')
  if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'home.html', {'shoes':shoes,'totalitem':totalitem})

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already = False
        if request.user.is_authenticated:
            item_already = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'productdetail.html',
                      {'product': product, 'item_already': item_already, 'totalitem': totalitem})

def allproducts(request , data=None):
  totalitem = 0
  if data == None:
    allproducts= Product.objects.filter(category='S')
  elif data == 'above':
    allproducts = Product.objects.filter(category='S').filter(selling_price__gt = 3000)
  elif data == 'below':
    allproducts = Product.objects.filter(category='S').filter(selling_price__lt = 3000)
  if request.user.is_authenticated:

      totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'product.html' ,{'allproducts': allproducts,'totalitem': totalitem})

def CustomerRegistrationView(request):
    form= CustomerRegistrationForm()

    if request.method == 'POST':
     form = CustomerRegistrationForm(request.POST)
     if form.is_valid():
         user = form.cleaned_data.get('username')
         messages.success(request,"Account Created for "+user)
         form.save()
         # return redirect('app/login.html')
     # ------- redirect to login page after succesful registration
    return render(request, 'register.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username , password=password)

        # -----check if user already exists---
        if user is not None:
            login(request, user)
            # messages.success(request, "Logged in " )
            return redirect('home')
        else:
            messages.warning(request, "Enter correct username/password..!")
    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect('home')




def address(request):
    return render(request,'address.html')

def addtocart(request):
    return render(request,'addtocart.html')

def base(request):
    return render(request,'base.html')

def buynow(request):
    return render(request,'buynow.html')

def changepassword(request):
    return render(request,'changepassword.html')

def checkout(request):
    return render(request,'checkout.html')

def newsview(request):
    return render(request,'news.html')

def customerregistration(request):
    return render(request,'customer registration.html')

def blogview(request):
    return render(request,'blog.html')

def loginview(request):
    return render(request,'login.html')

def productview(request):
    return render(request,'product.html')

def orders(request):
    return render(request,'orders.html')

def productdetail(request):
    return render(request,'productdetail.html')

@login_required
def Profile(request):
    form = CustomerProfileForm()
    totalitem = 0
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
    if form.is_valid():
        usr = request.user
        name = form.cleaned_data.get('name')
        locality = form.cleaned_data.get('locality')
        city = form.cleaned_data.get('city')
        zipcode = form.cleaned_data.get('zipcode')
        state = form.cleaned_data.get('state')
        reg = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode, state=state)

        reg.save()
        messages.success(request, "Profile updated sucessfully.. !")
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'profile.html', {'form': form,'totalitem':totalitem})



@login_required
def cartview(request):

    usr = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=usr, product=product).save()
    return redirect('showcart')

@login_required
def ShowCart(request):
    totalitem = 0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                total_amount = amount + shipping

            return render(request, 'addtocart1.html', {'carts':cart , 'total_amount':total_amount, 'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'emptycart.html')



def plus_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
           'quantity': c.quantity,
           'amount':amount,
            'total_amount': amount + shipping
                }
        return JsonResponse(data)


@login_required
def payment_done(request):
    totalitem = 0
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id =custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product = c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('/orders')



def minus_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
                'quantity': c.quantity,
                'amount':amount,
                'total_amount':amount + shipping
            }
        return JsonResponse(data)

def ProfileAddress(request):
    totalitem = 0
    add= Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'address.html', {'add':add,'totalitem':totalitem})

def orderView(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user= request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request , 'orders.html' , {'order_placed':op,'totalitem':totalitem})


def remove_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data = {
                'amount':amount,
                'total_amount':amount + shipping
            }
        return JsonResponse(data)

def Changepassword(request):
    totalitem = 0
    if request.method=="POST":
        old = request.POST["oldpassword"]
        new_pass = request.POST["newpassword"]

        user = User.objects.get(id=request.user.id)
        check = user.check_password(old)


        if check == True:
            user.set_password(new_pass)
            user.save()
            messages.success(request, "Password changed succesfully.. ")

        else:
            messages.warning(request, "Incorrect old password..")
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'changepassword.html',{'totalitem':totalitem})

@login_required
def checkoutView(request):
    user = request.user
    add = Customer.objects.filter(user=user)

    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
         for p in cart_product:
             tempamount = (p.quantity * p.product.selling_price)
             amount += tempamount
         totalamount = amount + shipping

    return render(request, 'checkout.html' ,{'add':add ,'totalamount':totalamount , 'cart_items':cart_items} )

def emptycartview(request):
    return render(request, 'emptycart.html')



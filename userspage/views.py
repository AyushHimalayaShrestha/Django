from django.shortcuts import render, redirect
from products.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
from django.views import View
import hmac
import hashlib
import uuid 
import base64

# Create your views here.

def index(request):
    products=Product.objects.all()[:8]
    context={
        'products':products
    }
    return render(request,'userpage/index.html',context)

def product_details(request,product_id):
    product=Product.objects.get(id=product_id)
    context={
        'product':product
    }
    return render(request,'userpage/productdetails.html',context)

def product_list(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'userpage/products.html',context)

def user_register(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Account Added')
            return redirect('/register')
        
        else:
            messages.add_message(request,messages.ERROR,'Please provide correct details')
            return render(request,'userpage/register.html',{'forms':form})
    context={
        'forms':UserCreationForm
    }
    return render(request,'userpage/register.html',context)

def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                if user.is_staff:
                    return redirect('/admin/dashboard')
                else:
                    return redirect('/')
                
                
            else:
                messages.add_message(request,messages.ERROR,'Please provide correct credentials')
                return render(request,'userpage/login.html',{'forms':form})
    context={
        'forms':LoginForm
    }
    return render(request,'userpage/login.html',context)

 #logout

def user_logout(request):
    logout(request)
    return redirect('/login')

@login_required
def add_to_cart(request,product_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    check_item_presence=Cart.objects.filter(product=product,user=user)
    if check_item_presence:
        messages.add_message(request,messages.ERROR,'Product is already present in the cart ')
        return redirect('/cart')
    else:
        cart=Cart.objects.create(product=product,user=user)
        if cart:
            messages.add_message(request,messages.SUCCESS,'Product Added to Cart')
            return redirect('/cart')
        else:
            messages.add_message(request,messages.ERROR,'Failed to Add to Cart')
            return redirect('/cart')
@login_required
def show_user_cart_item(request):
    user=request.user
    items=Cart.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request,'userpage/cart.html',context)

@login_required
def remove_cart(request,cart_id):
    cart=Cart.objects.get(id=cart_id)
    cart.delete()
    messages.add_message(request,messages.SUCCESS,'Product removed from cart')
    return redirect('/cart')

@login_required
def post_order(request,product_id,cart_id):
    user=request.user
    product=Product.objects.get(id=product_id)
    cart_item=Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            quantity=request.POST.get('quantity')
            price=product.product_price
            total_price=int(quantity)*int(price)
            contact_no=request.POST.get('contact_no')
            address=request.POST.get('address')
            payment_method=request.POST.get('payment_method')
            payment_status=request.POST.get('payment_status')
            order=Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status
            )
            if order.payment_method=='Cash on delivery':
                cart_item.delete()
                messages.add_message(request,messages.SUCCESS,'Order Successful')
                return redirect('/myorder')
            elif order.payment_method=='Esewa':
                return redirect(reverse('esewaform')+"?o_id="+str(order.id)+"&c_id="+str(cart_item.id))
            else:
                messages.add_message(request,messages.ERROR,'Failed to make an order')
                return render(request,'userpage/orderform.html',{'forms':form})
    context={
        'forms':OrderForm
    }
    return render(request,'userpage/orderform.html',context)


class EsewaView(View):
    def get(self,request,*agrs,**kwargs):
        o_id=request.GET.get('o_id')
        c_id=request.GET.get('c_id')
        cart=Cart.objects.get(id=c_id)
        order=Order.objects.get(id=o_id)

        uuid_val=uuid.uuid4()
        
        def genSha256(key,message): #(for encrypted message)
            key=key.encode('utf-8')
            message=message.encode('utf-8')
            
            hmac_sha256=hmac.new(key,message,hashlib.sha256)
            digest=hmac_sha256.digest()
            signature=base64.b64encode(digest).decode('utf-8')
            return signature
        secret_key='8gBm/:&EnhH.1/q'
        data_to_sign=f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
        result=genSha256(secret_key,data_to_sign)

        data={
            'amount':order.product.product_price,
            'total_amount':order.total_price,
            'transaction_uuid':uuid_val,
            'product_code':'EPAYTEST',
            'signature':result
        }

        context={
            'order':order,
            'data':data,
            'cart':cart
        }
        return render(request,'userpage/esewaform.html',context)
    
import json
@login_required
def esewa_verify(request,order_id,cart_id):
    if request.method=='GET':
        data=request.GET.get('data')
        decoded_data=base64.b64decode(data).decode('utf-8')
        map_data=json.loads(decoded_data)
        order=Order.objects.get(id=order_id)
        cart=Cart.objects.get(id=cart_id)

        if map_data.get('status') == 'COMPLETE':
            order.payment_status = True
            order.save()
            cart.delete()
            messages.add_message(request,messages.SUCCESS,'payment successful')
            return redirect('/myorder') 
        else:
            messages.add_message(request,messages.ERROR,'failed to make a payment')
            return redirect('/myorder')   

@login_required
def my_order(request):
    user=request.user
    items=Order.objects.filter(user=user)
    context={
        'items':items
    }
    return render(request,'userpage/myorder.html',context)

@login_required
def profile(request):
    user=User.objects.get(username=request.user)
    context={
        'user':user
    }
    return render(request,'userpage/profile.html',context)
@login_required
def update_profile(request):
    if request.method=='POST':
        form=ProfileUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Profile Updated')
            return redirect('/profile')
        else:
            messages.add_message(request,messages.ERROR('userpage/updateprofile.html',{'forms':form}))

        context={
            'forms':ProfileUpdateForm(instance=request.user)
        }    
        return render(request,'userpage/updateprofile.html',context)


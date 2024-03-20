from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Category
from django.contrib import messages
from .forms import CategoryForm,ProductForm
from django.contrib.auth.decorators import login_required
from userspage.auth import admin_only


# Create your views here.
@login_required
@admin_only
def index(request):
   products=Product.objects.all()
   context={
      'products':products
   }
   return render(request,'products/showproduct.html',context)

@login_required
@admin_only
def show_category(request):
   category=Category.objects.all()
   context={
      'category':category
   }
   return render(request,'products/showcategory.html',context)

# to delete category
@login_required
@admin_only
def delete_category(request,category_id):
   category=Category.objects.get(id=category_id)
   category.delete()
   messages.add_message(request,messages.SUCCESS,'Category Deleted')
   return redirect('/products/categorylist')

# to delete product
@login_required
@admin_only
def delete_product(request,product_id):
   product=Product.objects.get(id=product_id)
   product.delete()
   messages.add_message(request,messages.SUCCESS,'Product Deleted')
   return redirect('/products/list')


# to post category
@login_required
@admin_only
def post_category(request):
   if request.method == 'POST':
      form=CategoryForm(request.POST)
      if form.is_valid():
         form.save()
         messages.add_message(request,messages.SUCCESS,'Category Added')
         return redirect('/products/postcategory')
      else:
         messages.add_message(request,messages.ERROR,'Please verify form fields')
         return render(request,'products/addcategory.html',{'forms':form})

   context={
      'forms':CategoryForm
   }
   return render(request,'products/addcategory.html',context)

# to post product
@login_required
@admin_only
def post_product(request):
   if request.method == 'POST':
      form=ProductForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         messages.add_message(request,messages.SUCCESS,'Product Added')
         return redirect('/products/postproduct')
      else:
         messages.add_message(request,messages.ERROR,'Please verify form fields')
         return render(request,'products/addproduct.html',{'forms':form})
   context={
      'forms':ProductForm
   }
   return render(request,'products/addproduct.html',context)


#to update category
@login_required
@admin_only
def update_category(request,category_id):
   instance=Category.objects.get(id=category_id)

   if request.method == 'POST':
      form=CategoryForm(request.POST,instance=instance)

      if form.is_valid():
         form.save()
         messages.add_message(request,messages.SUCCESS,'Category Updated')
         return redirect('/products/categorylist')
      else:
         messages.add_message(request,messages.ERROR,'Please verify form fields')
         return render(request,'products/updatecategory.html',{'forms':form})


   context={
   
      'forms':CategoryForm(instance=instance)
   }
   return render(request,'products/updatecategory.html',context)

#to update product
@login_required
@admin_only
def update_product(request,product_id):
   instance=Product.objects.get(id=product_id)

   if request.method == 'POST':
      form=ProductForm(request.POST,request.FILES,instance=instance)

      if form.is_valid():
         form.save()
         messages.add_message(request,messages.SUCCESS,'Product Updated')
         return redirect('/products/list')
      else:
         messages.add_message(request,messages.ERROR,'Please verify form field')
         return render(request,'products/updateproduct.html',{'forms':form})
   
   context={
      'forms':ProductForm(instance=instance)
   }
   return render(request,'products/updateproduct.html',context)
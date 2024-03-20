from django.db import models

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=80,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name=models.CharField(max_length=100)  #metadata
    product_price=models.FloatField()
    stock=models.IntegerField()
    product_image=models.FileField(upload_to='static/uploads',null=True)
    product_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True) 
    

    def __str__(self):
        return self.product_name    
    
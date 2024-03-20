from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    PAYMENT=(
        ('Cash on Delivery','Cash on Delivery'),
        ('Esewa','Esewa')
    )    
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.IntegerField()
    delivery_status=models.CharField(default='Pending',max_length=100)
    payment_method=models.CharField(max_length=100,choices=PAYMENT)
    payment_status=models.BooleanField(default=False,null=True)
    contact_no = models.CharField(max_length=20)

    address=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
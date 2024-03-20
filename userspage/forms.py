from typing import Any
from django import forms
from .models import Order
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=['quantity','contact_no','address','payment_method']    

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm,self).__init__(*args,**kwargs)
        self.fields.pop('password',None)
        
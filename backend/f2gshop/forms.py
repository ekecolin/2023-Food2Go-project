from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import APIUser, Order, WeightTracking
from django.db import transaction

class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = APIUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password'}))

class OrderForm(ModelForm):
    name = forms.CharField(label="firstname", widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    sname = forms.CharField(label="surname", widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    shipping_address = forms.CharField(label="Shipping address", widget=forms.TextInput(attrs={'placeholder': 'Shipping Address'}))
    city = forms.CharField(label="city", widget=forms.TextInput(attrs={'placeholder': 'city'}))
    country = forms.CharField(label="country", widget=forms.TextInput(attrs={'placeholder': 'country'}))
    postcode = forms.CharField(label="postcode", widget=forms.TextInput(attrs={'placeholder': 'postcode'}))
    
    class Meta:
        model=Order
        #name, address, city, country and postcode
        fields = ['name', 'sname', 'shipping_address', 'city', 'country', 'postcode']

class WeightLossForm(ModelForm):
    class Meta:
        model = WeightTracking
        fields = ['weightkg']
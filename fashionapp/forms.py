from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from fashionapp.models import Customer


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality' , 'city', 'zipcode', 'state']
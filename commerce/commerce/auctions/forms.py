from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="email",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type":"email", "name":"email", "placeholder": "Email"}),
    )
    cellphone = forms.CharField(
        label="cellphone",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type":"text", "name":"cellphone", "placeholder": "Cellphone"}),
    )
    address = forms.CharField(
        label="address",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type":"text", "name":"address", "placeholder": "Address"}),
    )
    town = forms.CharField(
        label="town",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type":"text", "name":"town", "placeholder": "town"}),
    )
    country = forms.CharField(
        label="country",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type":"text", "name":"country", "placeholder": "country"}),
    )
    postcode = forms.CharField(
        label="postcode",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "type":"text", "name":"postcode", "placeholder": "postcode"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'cellphone', 'address', 'town', 'country', 'postcode']
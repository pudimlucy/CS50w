from email.policy import default
from unicodedata import name
from attr import attrs
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import NumberInput

from .models import User


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="email",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "name": "email",
            }
        ),
    )
    first_name = forms.CharField(
        label="first name",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
    )
    last_name = forms.CharField(
        label="last name",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
    )
    cellphone = forms.CharField(
        label="cellphone",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "cellphone",
            }
        ),
    )
    address = forms.CharField(
        label="address",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "address",
            }
        ),
    )
    town = forms.CharField(
        label="town",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "town",
            }
        ),
    )
    country = forms.CharField(
        label="country",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "country",
            }
        ),
    )
    postcode = forms.CharField(
        label="postcode",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "postcode",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "cellphone",
            "address",
            "town",
            "country",
            "postcode",
            "password1",
            "password2",
        ]


class NewListForm(forms.Form):
    item_title = forms.CharField(
        label="title",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "item_title",
                "placeholder": "Item title...",
            }
        ),
    )

    category = forms.ChoiceField(
        label="category",
        required=False,
        choices=(
            ("ETC", "Everything Else"),
            ("ANQ", "Antiques"),
            ("ART", "Art"),
            ("BBY", "Baby"),
            ("BKS", "Books"),
            ("BUS", "Bussiness & Industrial"),
            ("CAM", "Cameras & Photo"),
            ("CLP", "Cellphones"),
            ("CLT", "Clothing"),
            ("COL", "Collectibles"),
            ("CPT", "Computers"),
            ("CRL", "Consumer Eletronics"),
            ("CRT", "Crafts"),
            ("DOL", "Dolls & Bears"),
            ("DVD", "DVDs and Movies"),
            ("HLT", "Health & Beauty"),
            ("HOM", "Home & Garden"),
            ("JWL", "Jewerly & Watches"),
            ("MSC", "Music"),
            ("PET", "Pet Supplies"),
            ("PTR", "Pottery & Glasses"),
            ("RLS", "Real State"),
            ("SPC", "Speciality Services"),
            ("SPT", "Sporting Goods"),
            ("TOY", "Toys & Hobbies"),
            ("VDG", "Video Games & Consoles"),
        ),
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "category",
            }
        ),
    )

    image_link = forms.CharField(
        label="Image Link",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "image_link",
                "placeholder": "Image link...",
            }
        ),
    )

    start_price = (
        forms.DecimalField(
            label="Starting Price",
            required=True,
            decimal_places=2,
            min_value=0,
            widget=NumberInput(
                attrs={
                    "class": "form-control",
                    "type": "number",
                    "name": "image_link",
                    "min": "1",
                    "step": "any",
                }
            ),
        ),
    )

    quantity = forms.IntegerField(
        label="quantity",
        required=True,
        min_value=1,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "name": "quantity",
                "min": "1",
                "placeholder": "Quantity Available...",
            }
        ),
    )

    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={"class": "col-sm-11", "name": "description"}),
    )

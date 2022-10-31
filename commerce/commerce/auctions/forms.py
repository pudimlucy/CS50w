from email.policy import default
from unicodedata import name
from attr import attrs
from django import forms
from django.forms import NumberInput
from django.core.validators import RegexValidator

from .models import User


class CustomRegisterForm(forms.Form):

    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "username",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
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
        label="First Name",
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
        label="Last Name",
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
        label="Cellphone*",
        required=False,
        validators=[RegexValidator(r"^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$", "Please input a US phone number.")],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "cellphone",
            }
        ),
    )
    address = forms.CharField(
        label="Address",
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
        label="Town",
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
        label="Country",
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
        label="Postcode",
        required=True,
        validators=[RegexValidator(r"^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$", "Invalid postcode. If you think it should be valid, please contact our support.")],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "postcode",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password",
            }
        ),
    )
    confirmation = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "confirmation",
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
            "password",
            "confirmation",
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
        validators=[RegexValidator(r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)", "Invalid URL. Please provide the link to a jpeg or png.")],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "image_link",
                "placeholder": "Image link...",
            }
        ),
    )

    start_price = forms.DecimalField(
            label="Starting Price",
            required=True,
            decimal_places=2,
            min_value=0.01,
            widget=NumberInput(
                attrs={
                    "class": "form-control",
                    "type": "number",
                    "name": "image_link",
                    "min": "0.01",
                    "step": "any",
                }
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

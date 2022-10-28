from re import U
from django.contrib.auth.models import AbstractUser
from django.db import models


from django.contrib.auth.models import AbstractUser
from django.forms import DateTimeField
from django.db import models

# Django app that adds support for Money fields, access on https://github.com/django-money
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    """Custom User model - inherited from Django implementation"""
    balance = MoneyField(
        decimal_places=4,
        max_digits=19,
        default=5000,
        default_currency="USD",
    )
    cellphone = models.CharField(max_length=14)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    pass


class Listings(models.Model):
    """Model for product listing on Auditions"""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORIES = (
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
        ("ETC", "Everything Else"),
    )
    item_title = models.CharField(max_length=250)
    image_link = models.CharField(max_length=250)
    start_price = MoneyField(
        decimal_places=4,
        max_digits=19,
        default=0,
        default_currency="USD",
    )
    current_price = MoneyField(
        decimal_places=4,
        max_digits=19,
        default=0,
        default_currency="USD",
    )
    quantity = models.IntegerField()
    number_of_bids = models.IntegerField()
    bidders = models.IntegerField()
    watchers = models.IntegerField()
    start_date = models.DateField(auto_now_add=True, blank=True)


class Bids(models.Model):
    """Model for Bids on Auditions"""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_value = MoneyField(
        decimal_places=4,
        max_digits=19,
        default=0,
        default_currency="USD",
    )
    bid_date = models.DateField(auto_now_add=True)


class Comments(models.Model):
    """Model for Comments on Auditions"""

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)


class Watches(models.Model):
    """Model for Watches on Auditions"""

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

from email.policy import default
from re import U
from django.contrib.auth.models import AbstractUser
from django.db import models


from django.contrib.auth.models import AbstractUser
from django.forms import DateTimeField, DecimalField
from django.db import models

class User(AbstractUser):
    """Custom User model - inherited from Django implementation"""

    balance = DecimalField(
        decimal_places=2,
        max_digits=19,
        min_value=0,
    )
    cellphone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=16)
    pass


class Listings(models.Model):
    """Model for product listing on Auditions"""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    item_title = models.CharField(max_length=250)
    category = models.CharField(max_length=3, default=("ETC", "Everything Else"))
    image_link = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    start_price = models.DecimalField(
        decimal_places=2,
        max_digits=19,
        default=0.0,
    )
    current_price = models.DecimalField(
        decimal_places=2,
        max_digits=19,
        default=0.0,
    )
    quantity = models.IntegerField()
    number_of_bids = models.IntegerField()
    bidders = models.IntegerField()
    watchers = models.IntegerField()
    start_date = models.DateField(auto_now_add=True, blank=True)
    closed = models.BooleanField(default=False)


class Bids(models.Model):
    """Model for Bids on Auditions"""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_value = DecimalField(decimal_places=4, max_digits=19, min_value=0)
    bid_date = models.DateField(auto_now_add=True)


class Comments(models.Model):
    """Model for Comments on Auditions"""

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    time_sent = models.DateTimeField(auto_now_add=True)


class Watches(models.Model):
    """Model for Watches on Auditions"""

    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

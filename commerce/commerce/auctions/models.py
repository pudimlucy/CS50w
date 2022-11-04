from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model - inherited from Django implementation"""

    cellphone = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postcode = models.CharField(max_length=16)
    pass


class Listing(models.Model):
    """Model for product listing on Auditions"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_title = models.CharField(max_length=250)
    category = models.CharField(max_length=3, default=("ETC", "Everything Else"))
    image_link = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    start_price = models.DecimalField(
        decimal_places=2,
        max_digits=19,
        default=0.1,
    )
    start_date = models.DateField(auto_now_add=True, blank=True)
    close_date = models.DateTimeField(null=True, blank=True)


class Bid(models.Model):
    """Model for Bids on Auditions"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_value = models.DecimalField(decimal_places=2, max_digits=19)
    bid_date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    """Model for Comments on Auditions"""

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(null=True, blank=True)
    time_sent = models.DateTimeField(auto_now_add=True)


class Watch(models.Model):
    """Model for Watches on Auditions"""

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

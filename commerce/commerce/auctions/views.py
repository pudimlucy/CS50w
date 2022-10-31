import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings
from . import forms


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        nuform = forms.CustomRegisterForm(request.POST)
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "auctions/register.html",
                {
                    "message": "Passwords must match.",
                    "nuform": nuform,
                },
            )

        # Attempt to create new user
        if nuform.is_valid():
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            cellphone = request.POST["cellphone"]
            address = request.POST["address"]
            town = request.POST["town"]
            country = request.POST["country"]
            postcode = request.POST["postcode"]
            try:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    cellphone=cellphone,
                    address=address,
                    town=town,
                    country=country,
                    postcode=postcode,
                )
                user.save()
            except IntegrityError:
                return render(
                    request,
                    "auctions/register.html",
                    {
                        "message": "Username already taken.",
                        "nuform": nuform,
                    },
                )
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
            request,
            "auctions/register.html",
            {
                "message": "Invalid form, please try again.",
                "nuform":nuform,
            },
        )
    else:
        return render(
            request,
            "auctions/register.html",
            {
                "nuform": forms.CustomRegisterForm(),
            },
        )


@login_required(login_url="login")
def new_listing(request):

    if request.method == "POST":
        nlform = forms.NewListForm(request.POST)

        if nlform.is_valid():
            item_title = request.POST["item_title"]
            category = request.POST["category"]
            image_link = request.POST["image_link"]
            current_price = start_price = request.POST["start_price"]
            quantity = request.POST["quantity"]
            description = request.POST["description"]

            try:
                listing = Listings(
                    user_id=User.objects.get(pk=request.user.id),
                    item_title=item_title,
                    category=category,
                    image_link=image_link,
                    current_price=current_price,
                    start_price=start_price,
                    quantity=quantity,
                    description=description,
                    number_of_bids=0,
                    bidders=0,
                    watchers=0,
                )
                listing.save()
            except IntegrityError:
                return render(
                    request,
                    "auctions/new_listing.html",
                    {
                        "message": "An Integrity error occured, please try again.",
                        "nlform": nlform,
                    },
                )
        else:
            return render(
                request,
                "auctions/new_listing.html",
                {
                    "message": "Invalid Form, please try again.",
                    "nlform": nlform,
                },
            )
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request, "auctions/new_listing.html", {"nlform": forms.NewListForm()}
        )

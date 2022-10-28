import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
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
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
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
        username = request.POST["username"]
        email = request.POST["email"]
        cellphone = request.POST["cellphone"]
        address = request.POST["address"]
        town = request.POST["town"]
        country = request.POST["country"]
        postcode = request.POST["postcode"]
        try:
            user = User.objects.create_user(
                username=username,
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
                "nuform": forms.CustomRegisterForm(),
            },
        )


@login_required(login_url="login")
def new_listing(request):

    nlform = forms.NewListForm()

    if request.method == "POST":
        if nlform.is_valid():
            user_id = User.objects.get(id=request.user.id)
            item_title = request.POST["item-title"]
            category = request.POST["category"]
            image_link = request.POST["image_link"]
            current_price = starting_price = request.POST["starting_price"]
            quantity = request.POST["quantity"]
            description = request.POST["description"]

            listing = forms.NewListForm(
                user_id=user_id,
                item_title=item_title,
                category=category,
                image_link=image_link,
                current_price=current_price,
                starting_price=starting_price,
                quantity=quantity,
                description=description,
                number_of_bids=0,
                bidders=0,
                watchers=0,
            )
            listing.save()
            # TODO: load listing's page
            render(request, "auctions/index.html")
        else:
            render(
                request,
                "auctions/new_listing.html",
                {"nlform": nlform, "message": "Something went wrong, try again later."},
            )

    return render(request, "auctions/new_listing.html", {"nlform": nlform})

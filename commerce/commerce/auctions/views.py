import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Watches
from . import forms


def index(request):
    # Get all listings descending
    listings = Listings.objects.filter(closed=False).order_by("start_date")

    return render(request, "auctions/index.html", {"listings": listings})


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
                    "nuform": nuform,
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
            start_price = request.POST["start_price"]
            quantity = request.POST["quantity"]
            description = request.POST["description"]

            try:
                listing = Listings(
                    user_id=User.objects.get(pk=request.user.id),
                    item_title=item_title,
                    category=category,
                    image_link=image_link,
                    start_price=start_price,
                    quantity=quantity,
                    description=description,
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


@login_required(login_url="login")
def listing_page(request, item_id):
    try:
        listing = Listings.objects.get(pk=item_id)
        user = User.objects.get(pk=request.user.id)
    except Listings.DoesNotExist:
        return render(
            request, "auctions/index.html", {"message": "Auction doesn't exist."}
        )

    if request.user.is_authenticated:
        watch = Watches.objects.filter(
            listing_id=item_id, user_id=User.objects.get(id=request.user.id)
        ).first()

        if watch is None:
            watching = False
        else:
            watching = True
    else:
        watching = False

    return render(
        request,
        "auctions/listing_page.html",
        {
            "listing": listing,
            "user": user,
            "watching": watching,
        },
    )


@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":

        listing_id = request.POST.get("listing_id")
        listing = Listings.objects.get(id=listing_id)
        try:
            ...
        except Listings.DoesNotExist:
            return render(
                request, "auctions/index.html", {"message": "Auction doesn't exist"}
            )

        user = User.objects.get(pk=request.user.id)

        if request.POST.get("watching") == "True":
            delete = Watches.objects.filter(
                user_id=user,
                listing_id=listing,
            )
            delete.delete()
        else:
            try:
                save = Watches(user_id=user, listing_id=listing)
                save.save()
            except IntegrityError:
                return render(
                    request,
                    "auctions/index.html",
                    {"message": "Auction is already on your watchlist"},
                )
        return HttpResponseRedirect("/" + listing_id)

    watchlist_ids = Watches.objects.filter(user_id=request.user.id).values_list(
        "listing_id"
    )
    watchlist_items = Listings.objects.filter(id__in=watchlist_ids)

    return render(request, "auctions/watchlist.html", {"watchlist": watchlist_items})

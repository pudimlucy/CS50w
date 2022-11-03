import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Watches, Bids
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
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def new_listing(request):

    if request.method == "POST":
        nlform = forms.NewListForm(request.POST)

        if nlform.is_valid():
            item_title = request.POST["item_title"]
            category = request.POST["category"]
            image_link = request.POST["image_link"]
            start_price = request.POST["start_price"]
            description = request.POST["description"]

            try:
                listing = Listings(
                    user=User.objects.get(pk=request.user.id),
                    item_title=item_title,
                    category=category,
                    image_link=image_link,
                    start_price=start_price,
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
            request,
            "auctions/index.html",
            {"message": "Invalid request. Please login."},
        )

    if request.user.is_authenticated:
        watch = Watches.objects.filter(listing=item_id, user=user).first()

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
            "seller": User.objects.filter(id=listing.user.id).first(),
            "watching": watching,
            "bform": forms.BidForm(),
            "current_price": Bids.objects.filter(listing=listing).order_by("-bid_value").first().bid_value,
            "bids_made": len(Bids.objects.filter(listing=listing))
        },
    )


@login_required(login_url="login")
def watchlist(request):
    if request.method == "POST":

        try:
            listing_id = request.POST.get("listing_id")
            listing = Listings.objects.get(id=listing_id)
            user = User.objects.get(pk=request.user.id)
        except Listings.DoesNotExist:
            return render(
                request,
                "auctions/index.html",
                {"message": "Invalid request. Please login."},
            )

        if request.POST.get("watching") == "True":
            watching = Watches.objects.filter(
                user=user,
                listing=listing,
            )
            watching.delete()
        else:
            try:
                watching = Watches(
                    user=user,
                    listing=listing,
                )
                watching.save()
            except IntegrityError:
                return render(
                    request,
                    "auctions/index.html",
                    {"message": "Auction is already on your watchlist"},
                )
        return HttpResponseRedirect("/" + listing_id)

    watchlist_list = Watches.objects.filter(user=request.user).values_list("listing")
    watchlist = Listings.objects.filter(id__in=watchlist_list)

    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})


@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        try:
            listing_id = request.POST.get("listing_id")
            listing = Listings.objects.get(id=listing_id)
            user = User.objects.get(pk=request.user.id)
        except Listings.DoesNotExist:
            return render(
                request,
                "auctions/index.html",
                {"message": "Invalid request. Please login."},
            )

        if user == listing.user:
            return render(
                request, "auctions/index.html", {"message": "Invalid request."}
            )

        bform = forms.BidForm(request.POST)
        if bform.is_valid():
            bid_value = float(request.POST["bid_value"])
            highest = (
                Bids.objects.filter(listing=listing).order_by("-bid_value").first()
            )
            if (
                highest is None and bid_value > listing.start_price
            ) or bid_value > float(highest.bid_value):
                try:
                    bid = Bids(
                        user=user,
                        listing=listing,
                        bid_value=bid_value,
                    )
                    bid.save()
                except IntegrityError:
                    return render(
                        request,
                        "auctions/index.html",
                        {
                            "message": "An Integrity error occured, please try again.",
                        },
                    )
            else:
                return render(
                    request,
                    "auctions/index.html",
                    {
                        "message": "Please bid a value higher than the listing's current value.",
                    },
                )
        else:
            return render(
                request,
                "auctions/index.html",
                {
                    "message": "Invalid Form, please try again.",
                },
            )
        return HttpResponseRedirect("/" + listing_id)
    # TODO: display user's bids on GET request
    return HttpResponseRedirect("/")

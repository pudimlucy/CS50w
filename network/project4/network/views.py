import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserFollowing
from .forms import NewPostForm


def index(request):
    return render(request, "network/index.html")


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
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="login")
def new_post(request):
    # Checks for method
    if request.method == "POST":
        # Gets forms content
        npform = NewPostForm(request.POST)
        if npform.is_valid():
            try:
                content = request.POST["post"]
                author = request.user

                # Saves new post
                post = Post(content=content, author=author)
                post.save()
            except IntegrityError:
                return render(
                    request,
                    "network/new_post.html",
                    {
                        "message": "An Integrity error occured, please try again.",
                        "npform": npform,
                    },
                )
        else:
            return render(
                request,
                "network/new_post.html",
                {
                    "message": "Invalid Form, please try again.",
                    "npform": npform,
                },
            )
        return HttpResponseRedirect(reverse("index"))
    # Renders new post page
    return render(request, "network/new_post.html", {"npform": NewPostForm()})


def display_posts(request, filter):
    # Gets filtered posts
    if filter == "all":
        posts = Post.objects.all()
    else:
        user = User.objects.filter(username=filter).first()
        posts = Post.objects.filter(author=user.id)

    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)


def get_user(request, username):
    user = User.objects.filter(username=username).first()
    return JsonResponse(user.serialize(), safe=False)


@login_required(login_url="login")
def view_profile(request, username):
    profile = User.objects.filter(username=username).first()
    user = User.objects.get(pk=request.user.id)
    if profile is None:
        return HttpResponseRedirect(reverse("index"))
    
    if request.user.is_authenticated:
        relation = UserFollowing.objects.filter(follower=user, following=profile).first()
        following = False if relation is None else True
    else:
        following = False

    if request.user.is_authenticated:
        return render(
            request,
            "network/user.html",
            {
                "user": user,
                "profile": profile,
                "nfollowing": len(profile.follows()),
                "nfollowers": len(profile.followers()),
                "following": following,
            },
        )

@login_required(login_url="login")
def follow(request):
    if request.method == "POST":
        profile = request.POST.get("profile_id")
        profile = User.objects.filter(id=profile).first()
        if profile is None:
            return HttpResponseRedirect(reverse("index"))
        user = User.objects.get(pk=request.user.id)

        if request.POST.get("following") == "True":
            relation = UserFollowing.objects.filter(
                follower = user,
                following = profile,
            ).first()
            relation.delete()
        else:
            try:
                relation = UserFollowing(
                    follower = user,
                    following = profile,
                )
                relation.save()
            except IntegrityError:
                return render(
                request,
                "network/index.html",
                {
                    "message": "An Integrity error occured, please try again.",
                },
            )
        return HttpResponseRedirect("/profile/" + profile.username)
    else:
        return HttpResponseRedirect(reverse("index"))

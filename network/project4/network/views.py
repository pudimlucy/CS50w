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
def profile_view(request, username):
    # Gets user and profile
    profile = User.objects.filter(username=username).first()
    user = User.objects.get(pk=request.user.id)

    # Profile does not exist
    if profile is None:
        return HttpResponseRedirect(reverse("index"))

    # Checks for following
    if request.user.is_authenticated:
        relation = UserFollowing.objects.filter(
            follower=user, following=profile
        ).first()
        following = False if relation is None else True
    else:
        following = False

    # Renders profile page
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
def following_view(request, username):
    # Checks if logged in user is following/<username>
    check = User.objects.filter(username=username).first()
    user = User.objects.get(pk=request.user.id)
    if check is None or check != user:
        return HttpResponseRedirect(reverse("index"))
    # Renders following page
    return render(
        request,
        "network/following.html",
    )


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


def edit_post(request, id):
    if request.method == "PUT":
        # Gets post
        post = Post.objects.filter(id=id).first()
        # Checks user
        if request.user != post.author:
            return HttpResponse("Invalid request", status=403)

        # Updates post
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()

        # Returns updated post data
        return JsonResponse(post.serialize())
    else:
        return HttpResponse("Invalid request", status=403)


@login_required(login_url="login")
def follow(request):
    if request.method == "POST":
        # Gets profile and user
        profile = User.objects.filter(id=request.POST.get("profile_id")).first()
        user = User.objects.get(pk=request.user.id)
        if profile or user is None:
            return HttpResponse("Invalid request", status=403)

        # Checks user-profile relation
        if request.POST.get("following") == "True":
            # Unfollows
            relation = UserFollowing.objects.filter(
                follower=user,
                following=profile,
            ).first()
            relation.delete()
        elif user != profile:
            # Follows
            try:
                relation = UserFollowing(
                    follower=user,
                    following=profile,
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
        else:
            return HttpResponse("Invalid request", status=403)
        return HttpResponseRedirect("/profile/" + profile.username)
    else:
        return HttpResponse("Invalid request", status=403)


def get_user(request, username):
    # Gets user
    user = User.objects.filter(username=username).first()
    # Returns user's data
    return JsonResponse(user.serialize(), safe=False)


def get_logged_user(request):
    # Returns user's data if logged in
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        return JsonResponse(user.serialize(), safe=False)
    # Empty response otherwise
    else:
        return JsonResponse(None, safe=False)


def get_post(request, id):
    post = Post.objects.filter(id=id).first()
    return JsonResponse(post.serialize())


def get_all_posts(request):
    # Gets posts
    posts = Post.objects.all()
    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)


def get_user_posts(request, username):
    # Gets user's posts
    user = User.objects.filter(username=username).first()
    posts = Post.objects.filter(author=user.id)
    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)


def get_following_posts(request, username):
    # Get's users follows
    user = User.objects.filter(username=username).first()
    relations = UserFollowing.objects.filter(follower=user).all()

    profiles = []
    for relation in relations:
        profiles.append(relation.following.id)

    # Gets posts made by user's follows sorted by date
    profiles = User.objects.filter(pk__in=profiles).all()
    posts = Post.objects.filter(author__in=profiles).order_by("-date")

    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)

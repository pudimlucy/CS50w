import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserFollowing, Interaction
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
    try:
        profile = User.objects.get(username=username)
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
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
    try:
        check = User.objects.get(username=username)
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    if check != user:
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
                post = Post(
                    content=content, author=author, date=datetime.datetime.now()
                )
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
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return HttpResponse("Invalid request", status=403)
        # Checks user
        if request.user != post.author:
            return HttpResponse("Invalid request", status=403)

        # Updates post
        data = json.loads(request.body)
        post.content = data["content"]
        post.date = post.date
        post.save()

        # Returns updated post data
        return JsonResponse(post.serialize())
    else:
        return HttpResponse("Invalid request", status=403)


@login_required(login_url="login")
def follow(request):
    if request.method == "POST":
        # Gets profile and user
        try:
            profile = User.objects.get(id=request.POST.get("profile_id"))
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return HttpResponse("Invalid request", status=403)

        # Checks user-profile relation
        if request.POST.get("following") == "True":
            # Unfollows
            relation = UserFollowing.objects.get(
                follower=user,
                following=profile,
            )
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
            return HttpResponse(status=200)
        return HttpResponseRedirect("/profile/" + profile.username)
    else:
        return HttpResponse("Invalid request", status=403)


@login_required(login_url="login")
def interact(request):
    data = json.loads(request.body)

    try:
        post = Post.objects.get(pk=data['id'])
    except Post.DoesNotExist:
        return HttpResponse("Invalid request", status=403)
    
    try:
        interacted = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return HttpResponse("Invalid request", status=403)
    
    try:
        if data['type'] not in ["like", "dislike"]:
            raise IntegrityError
        else:
            type = (data['type']=="like")
    except IntegrityError:
        return HttpResponse("Integrity error", status=403) 
    
    try:
        interaction = Interaction.objects.get(post=post, interacted=interacted)
    except:
        interaction = Interaction(
                post=post, interacted=interacted, type=type
            )
        interaction.save()
        return HttpResponse(status=200)
    else:
        interaction.delete()    
        if interaction.type == type:
            return HttpResponse(status=200)
        else:
            interaction = Interaction(
                post=post, interacted=interacted, type=type
            )
            interaction.save()
            return HttpResponse(status=200)


def get_user(request, username):
    # Gets user
    user = User.objects.get(username=username)
    # Returns user's data
    return JsonResponse(user.serialize(), safe=False)


def get_logged_user(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        return JsonResponse(user.serialize(), safe=False)
    # Empty response otherwise
    else:
        return JsonResponse(None, safe=False)
        


def get_post(request, id):
    # Returns post's data if it exists
    try:
        post = Post.objects.get(id=id)
    # Empty response otherwise
    except User.DoesNotExist:
        return JsonResponse(None, safe=False)
    return JsonResponse(post.serialize())


def get_all_posts(request):
    # Gets posts
    posts = Post.objects.all()
    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)


def get_user_posts(request, username):
    # Gets user's posts
    try:
        user = User.objects.get(username=username)
    # Empty response if no user
    except User.DoesNotExist:
        return JsonResponse(None, safe=False)
    posts = Post.objects.filter(author=user.id).all()
    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)


def get_following_posts(request, username):
    # Get's users follows
    try:
        user = User.objects.get(pk=request.user.id)
        check = User.objects.get(username=username)
        if user != check:
            raise User.DoesNotExist
    # Empty response if no user
    except User.DoesNotExist:
        return JsonResponse(None, safe=False)
    relations = UserFollowing.objects.filter(follower=user).all()

    profiles = []
    for relation in relations:
        profiles.append(relation.following.id)

    # Gets posts made by user's follows sorted by date
    profiles = User.objects.filter(pk__in=profiles).all()
    posts = Post.objects.filter(author__in=profiles).order_by("-date")

    # Returns posts
    return JsonResponse([post.serialize() for post in posts], safe=False)

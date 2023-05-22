from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.view_profile),
    path("follow", views.follow, name="follow"),
    path("following/<str:username>", views.following, name="following"),
    # API Routes
    path("posts/<str:filter>", views.get_posts, name="posts"),
    path("user/<str:username>", views.get_user, name="user"),
    path("follows/<str:username>", views.get_follows, name="follows")
]

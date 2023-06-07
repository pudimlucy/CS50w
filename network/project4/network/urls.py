from django.urls import path

from . import views

urlpatterns = [
    # views
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("following/<str:username>", views.following_view, name="following"),
    # user functionality
    path("new_post", views.new_post, name="new_post"),
    path("edit_post/<int:id>", views.edit_post, name="edit"),
    path("follow", views.follow, name="follow"),
    # API Routes
    path("user/<str:username>", views.get_user, name="user"),
    path("logged_user", views.get_logged_user, name="logged_user"),
    path("post/<int:id>", views.get_post, name="post"),
    path("posts", views.get_all_posts, name="all_posts"),
    path("userposts/<str:username>", views.get_user_posts, name="user_posts"),
    path("follows/<str:username>", views.get_following_posts, name="following_posts"),
]

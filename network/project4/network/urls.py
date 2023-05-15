from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),

    # API Routes
    # path("posts/<int:post_id>", views.display_post, name="post"),
    path("posts/<str:posts>", views.display_posts, name="posts")
]

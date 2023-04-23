from django.urls import path
from django.contrib import admin


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:item_id>", views.listing_page, name="listing_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categories_page, name="categories_page"),
]

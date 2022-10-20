from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.page, name="title"),
    path("wiki/search/", views.get_search, name="search"),
    path("/new", views.new, name="new"),
    path("/edit", views.edit, name="edit"),
    path("/save", views.save, name="save"),
    path("/random", views.random, name="random"),
]

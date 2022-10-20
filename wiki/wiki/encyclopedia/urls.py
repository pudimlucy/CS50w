from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="title"),
    path("wiki/search/", views.get_search, name="search"),
    path("wiki/new", views.new, name="new"),
    path("wiki/edit", views.edit, name="edit"),
    path("wiki/random", views.random, name="random"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/new", views.new, name="new"),
    path("/edit", views.edit, name="edit"),
    path("wiki/<str:title>", views.page, name="title"),
    path("wiki/search/", views.get_search, name="search"),
]

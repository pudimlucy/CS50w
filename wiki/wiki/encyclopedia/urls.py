from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="title"),
    path("wiki/<str:search>", views.get_search, name="search"),
]

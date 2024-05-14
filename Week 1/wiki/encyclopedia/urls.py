from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_page, name = "title"),
    path("search/", views.searchEntry, name = 'search'),
    path("create/", views.create, name = "create"),
    path("edit/", views.edit, name = "edit"),
    path("random/", views.random, name = "random")
]

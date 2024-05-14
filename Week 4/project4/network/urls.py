
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name = "newPost"),
    path("following", views.following, name = "following"),
    path("profile/<str:username>", views.profile, name = "profile"),
    path("follow/<int:username>", views.follow, name = "follow"),
    path("unfollow/<int:username>", views.unfollow, name = "unfollow"),
    path("edit/<int:id>", views.edit, name = "edit"),
    path("unlike/<int:id>", views.unlike, name = "unlike"),
    path("like/<int:id>", views.like, name = "like")
]

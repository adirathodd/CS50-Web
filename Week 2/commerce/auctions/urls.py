from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.newListing, name = "create"),
    path("listing", views.listing, name = "listing"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("removeWL", views.removeWL, name = "removeWL"),
    path("addWL", views.addWL, name = "addWL"),
    path("addComment", views.addComment, name = "addComment"),
    path("bid/<int:id>", views.bid, name = "bid"),
    path("closeListing/<int:id>", views.closeAuction, name = "closeListing")
]

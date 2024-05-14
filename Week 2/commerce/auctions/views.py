from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comments, Bid


def index(request):
    if request.method == "GET":
        categories = Category.objects.all()
        listings = Listing.objects.filter(active = True)
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories
        })
    else:
        category = request.POST['cat']
        categories = Category.objects.all()
        if category != "all":
            catData = Category.objects.get(catName = category)
            listings = Listing.objects.filter(active = True, category = catData)
            return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories
            })
        categories = Category.objects.all()
        listings = Listing.objects.filter(active = True)
        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": categories
        })

def listing(request):
    id = request.POST["listing"]
    listing1 = Listing.objects.get(pk = id)
    currentUser = request.user
    onWatchList = currentUser in listing1.watchList.all()
    comments = Comments.objects.filter(listing = listing1)
    if listing1.active == False:
        return render(request, "auctions/listing.html", {
        "listing": listing1,
        "onWatchList": onWatchList,
        "comments": comments,
        "isOwner": currentUser.username == listing1.owner.username,
        "message": "Congratulations! You have won this item."
    })
    return render(request, "auctions/listing.html", {
        "listing": listing1,
        "onWatchList": onWatchList,
        "comments": comments,
        "isOwner": currentUser.username == listing1.owner.username
    })
    

def watchlist(request):
    userCurrent = request.user
    listings = userCurrent.onWatchList.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removeWL(request):
    id = request.POST["id"]
    listing = Listing.objects.get(pk = id)
    currentUser = request.user
    listing.watchList.remove(currentUser)
    comments = Comments.objects.filter(listing = listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "onWatchList": False,
        "comments": comments,
        "isOwner": currentUser.username == listing.owner.username
    })

def addWL(request):
    id = request.POST["id"]
    listing = Listing.objects.get(pk = id)
    currentUser = request.user
    listing.watchList.add(currentUser)
    comments = Comments.objects.filter(listing = listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "onWatchList": True,
        "comments": comments,
        "isOwner": currentUser.username == listing.owner.username
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
       return render(request, "auctions/register.html")

def newListing(request):
    if (request.method == "GET"):
        categories = Category.objects.all()
        return render(request, "auctions/newListing.html", {
            "categories": categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        price = int(request.POST['price'])
        imageURL = request.POST['image']
        category = request.POST['cat']
        catData = Category.objects.get(catName = category)
        user = request.user

        bid1 = Bid(bid2 = price, user = request.user)
        bid1.save()

        listingNew = Listing(owner = user, title = title, description = description, price = bid1, image = imageURL, category = catData)
        listingNew.save()
        return HttpResponseRedirect(reverse("index"))

def addComment(request):
    id = request.POST['id']
    currentUser = request.user
    listing = Listing.objects.get(pk = id)
    message = request.POST['comment']

    comment = Comments(
        writer = currentUser,
        listing = listing,
        message = message
    )
    comment.save()
    onWatchList = currentUser in listing.watchList.all()
    comments = Comments.objects.filter(listing = listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "onWatchList": onWatchList,
        "comments": comments,
        "isOwner": currentUser.username == listing.owner.username
    })

def bid(request, id):
    user = request.user
    bid = request.POST['bid']
    listing = Listing.objects.get(pk=id)
    newBid = Bid(bid2 = bid, user = user)
    newBid.save()
    listing.price = newBid
    listing.save()
    currentUser = request.user
    onWatchList = currentUser in listing.watchList.all()
    comments = Comments.objects.filter(listing = listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "onWatchList": onWatchList,
        "comments": comments,
        "message": "Successful bid",
        "isOwner": currentUser.username == listing.owner.username
    })

def closeAuction(request, id):
    listing = Listing.objects.get(pk=id)
    listing.active = False
    listing.save()
    winner = listing.price
    currentUser = request.user
    onWatchList = currentUser in listing.watchList.all()
    comments = Comments.objects.filter(listing = listing)
    if currentUser.username == listing.price.user.username:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "onWatchList": onWatchList,
        "comments": comments,
        "message": f"You have won this item for a price of ${winner.bid2}"
    })
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "onWatchList": onWatchList,
        "comments": comments,
        "message": f"{winner.user} has won this item for a price of ${winner.bid2}"
    })

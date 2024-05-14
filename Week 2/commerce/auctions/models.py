from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    catName = models.CharField(max_length = 20)

    def __str__(self):
        return self.catName

class Bid(models.Model):
    bid2 = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bidder")


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
    active = models.BooleanField(default = True)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    price = models.ForeignKey(Bid, on_delete = models.CASCADE, blank = True, null = True, related_name = "bid1")
    image = models.CharField(max_length = 1000, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "category", blank = True)
    watchList = models.ManyToManyField(User, blank = True, related_name = "onWatchList")
    
    def __str__(self):
        return self.title
    
class Comments(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "writer")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "listing")
    message = models.CharField(max_length = 500)
    

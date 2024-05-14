from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
    postText = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add= True)
    postLikes =  models.IntegerField(default = 0)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "post")


class Follow(models.Model):
    userFollowing = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userFollowing")
    userFollower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userFollower")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "likeUser")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "likePost")
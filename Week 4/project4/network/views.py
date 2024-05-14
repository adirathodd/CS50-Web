from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, Post, Follow, Like
from django.core.paginator import Paginator

def index(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by('-timestamp')
        print(posts)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        postsOfPage = paginator.get_page(page_number)

        currentUser = request.user
        likedPosts = Like.objects.all()
        currentUserLiked = []
        try:
            for like in likedPosts:
                if like.user.id == currentUser.id:
                    currentUserLiked.append(like.post.id)
        except:
            currentUserLiked = []
        return render(request, "network/index.html", {
            "posts": postsOfPage,
            "likedPosts": currentUserLiked
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request):
    if request.method == "GET":
        return render(request, "network/newPost.html")
    else:
        user = request.user
        text = request.POST['postText']

        newPost = Post(user = user, postText = text)
        newPost.save()
        return HttpResponseRedirect(reverse('index'))
    
def following(request):
    if request.method == "GET":
        currentUser = request.user
        userData = User.objects.get(pk = currentUser.id)

        following = Follow.objects.filter(userFollowing = currentUser)
        posts = Post.objects.all().order_by('-timestamp')
        followingPosts = []

        for post in posts:
            for person in following:
                if person.userFollower == post.user:
                    followingPosts.append(post)

        paginator = Paginator(followingPosts, 10)
        page_number = request.GET.get('page')
        postsOfPage = paginator.get_page(page_number)

        currentUser = request.user
        likedPosts = Like.objects.all()
        currentUserLiked = []
        try:
            for like in likedPosts:
                if like.user.id == currentUser.id:
                    currentUserLiked.append(like.post.id)
        except:
            currentUserLiked = []

        return render(request, "network/following.html", {
            "posts": postsOfPage,
            "likedPosts": currentUserLiked
        }) 
    
def follow(request, username):
    if request.method == "POST":
        userFollowing = request.user
        userFollower = request.POST['userFollowing']
        follower = User.objects.get(pk = userFollower)

        a = Follow(userFollowing = userFollowing, userFollower = follower)
        a.save()
        return HttpResponseRedirect(reverse(profile, kwargs = {"username": username}))
    
def unfollow(request, username):
    if request.method == "POST":
        userUnfollowing = request.user
        userUnfollower = request.POST['userUnfollowing']
        unfollower = User.objects.get(pk = userUnfollower)

        a = Follow.objects.get(userFollowing = userUnfollowing, userFollower = unfollower)
        a.delete()
        return HttpResponseRedirect(reverse(profile, kwargs = {"username": unfollower.id }))

    
def profile(request, username):
    if request.method == "GET":
        user = User.objects.get(pk = username)
        posts = Post.objects.filter(user = username).order_by('-timestamp')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        postsOfPage = paginator.get_page(page_number)

        followers = Follow.objects.filter(userFollower = user)
        following = Follow.objects.filter(userFollowing = user)
        isFollowing = False
        try:
            check = followers.filter(userFollowing = User.objects.get(pk = request.user.id))
            if len(check) > 0:
                isFollowing = True
            else:
                isFollowing = False
        except:
            isFollowing = False

        currentUser = request.user
        likedPosts = Like.objects.all()
        currentUserLiked = []
        try:
            for like in likedPosts:
                if like.user.id == currentUser.id:
                    currentUserLiked.append(like.post.id)
        except:
            currentUserLiked = []
        return render(request, "network/profile.html", {
            "posts": postsOfPage,
            "user1": user,
            "followers": followers,
            "following": following,
            "isFollowing": isFollowing,
            "likedPosts": currentUserLiked
        })

def edit(request, id):
    if (request.method == "POST"):
        newPost = json.loads(request.body)
        ogPost = Post.objects.get(pk = id)
        ogPost.postText = newPost['postText']
        ogPost.save()
        return HttpResponseRedirect(reverse("index"))
    
def unlike(request, id):
    post = Post.objects.get(pk = id)
    post.postLikes -= 1
    post.save()
    like = Like.objects.get(post = post)
    filterLike = Like.objects.filter(user = User.objects.get(pk = request.user.id), post = post)
    filterLike.delete()
    return JsonResponse({"message": "unliked", "likes": post.postLikes})
    
def like(request, id):
    post = Post.objects.get(pk = id)
    post.postLikes += 1
    post.save()
    user = User.objects.get(pk = request.user.id)
    like = Like(user = user, post = post)
    like.save()
    return JsonResponse({"message": "liked", "likes": post.postLikes})
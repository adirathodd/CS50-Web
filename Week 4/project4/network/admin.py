from django.contrib import admin
from .models import Follow, Post, User, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)
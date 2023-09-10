from home.models import ChatRoom, Comment, Friend, Genre, Message, Post, Profile, imageUpload
from django.contrib import admin

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Friend)
admin.site.register(Message)
admin.site.register(ChatRoom)
admin.site.register(imageUpload)
admin.site.register(Genre)

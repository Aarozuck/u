from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('follow/user/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
    path('feed/', views.feed, name='feed'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('add_post/', views.add_post, name='add_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    #chat
    path('chathome/',views.chat_home ,name='chathome'),
    path('friends/', views.friends_list, name='friends_list'),
    path('chatrooms/', views.chatroom_list, name='chatroom_list'),
    path('chatroom/<int:chatroom_id>/', views.chatroom, name='chatroom'),
    path('message/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('message/reply/<int:message_id>/', views.reply_message, name='reply_message'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('chatroom/delete/<int:chatroom_id>/', views.delete_chatroom, name='delete_chatroom'),
    #meme
    path('meme/',views.home,name='home'),
    path('home/<str:pk>/',views.homeFilter,name='homefilter'),
    path('upload-image/',views.upload_image,name='upload-image'),
    path('about/',views.about,name='about'),
    #search
     path('search/', views.search_view, name='search'),
]

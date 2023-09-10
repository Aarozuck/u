from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import  ImageUploadForm, MessageForm, PostForm, UserProfileForm, UserRegistrationForm, UserLoginForm
from .models import ChatRoom, Friend, Genre, Message, Profile, Post, Comment,User, imageUpload
from django.contrib import messages
from django.db.models import Q
from typing import NoReturn
from django.shortcuts import render



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = Profile(user=user, bio=form.cleaned_data['bio'], info=form.cleaned_data['info'],
                              phone_number=form.cleaned_data['phone_number'],
                              profile_picture=form.cleaned_data['profile_picture'])
            profile.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login.html')

@login_required
def profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(user=request.user)
    followers_count = profile.followers.count()
    following_count = profile.following.count()
    return render(request, 'profile.html', {'profile': profile, 'posts': posts,
                                                       'followers_count': followers_count,
                                                       'following_count': following_count})

@login_required
def follow_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)
    request.profile.following.add(user)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user = get_object_or_404(Profile, id=user_id)
    request.profile.following.remove(user)
    return redirect('profile', user_id=user_id)
    
@login_required
def feed(request):
    posts = Post.objects.all().order_by('likes')
    return render(request, 'feed.html', {'posts': posts})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        post.content = content
        post.save()
        return redirect('feed')
    return render(request, 'edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('feed')

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes.add(request.user)
    return redirect('feed')

@login_required
def dislike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.dislikes.add(request.user)
    return redirect('feed')

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment(post=post, user=request.user, content=content)
        comment.save()
        return redirect('feed')
    return render(request, 'add_comment.html', {'post': post})
def edit_profile_view(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=Profile)
    return render(request, 'edit_profile.html', {'form': form})

    #chat views

@login_required
def chat_home(request):
    return render(request,'chat/chathome.html')    

@login_required
def friends_list(request):
    friends = Friend.objects.get(current_user=request.user)
    return render(request, 'chat/friends_list.html', {'friends': friends})

@login_required
def chatroom_list(request):
    chatrooms = ChatRoom.objects.filter(members=request.user)
    return render(request, 'chat/chatroom_list.html', {'chatrooms': chatrooms})

@login_required
def chatroom(request, chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chatroom = chatroom
            message.save()
            return redirect('chatroom', chatroom_id=chatroom_id)
    else:
        form = MessageForm()
    return render(request, 'chat/chatroom.html', {'chatroom': chatroom, 'messages': messages, 'form': form})

@login_required
def edit_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('chatroom', chatroom_id=message.chatroom.id)
    else:
        form = MessageForm(instance=message)
    return render(request, 'chat/edit_message.html', {'form': form})

@login_required
def reply_message(request, message_id):
    parent_message = Message.objects.get(id=message_id)
    chatroom_id = parent_message.chatroom.id
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chatroom = parent_message.chatroom
            message.parent = parent_message
            message.save()
            return redirect('chatroom', chatroom_id=chatroom_id)
    else:
        form = MessageForm()
    return render(request, 'chat/reply_message.html', {'parent_message': parent_message, 'form': form})

@login_required
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    chatroom_id = message.chatroom.id
    message.delete()
    return redirect('chatroom', chatroom_id=chatroom_id)

@login_required
def delete_chatroom(request, chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    chatroom.delete()
    return redirect('chat/chatroom_list')    

#meme    

def home(request):
    page = 'gallery'
    search_item = request.GET.get('search_item') if request.GET.get('search_item') != None else ''
    
    images = imageUpload.objects.filter(
            Q(title__icontains = search_item)|
            Q(genre__title__icontains = search_item)
        ).order_by('-created')
    genres = Genre.objects.all()
    context = {'images':images,'genres':genres,'page':page}
    return render(request,'meme/home.html',context)

@login_required(login_url='login')
def upload_image(request):
    page = 'upload'
    genres = Genre.objects.all()
    form = ImageUploadForm()
    if request.method == 'POST':
        title = request.POST.get('title')
        genre_title = request.POST.get('genre_title')
        genre,created = Genre.objects.get_or_create(title=genre_title)
        image = request.FILES.get('image')
        obj = imageUpload.objects.create(
            user = request.user,
            title = title,
            genre = genre,
            image = image
        )
        obj.save()
        # form = ImageUploadForm(request.POST,request.FILES)
        # if form.is_valid():
        #     form.save()
        messages.success(request, 'Image has been successfully uploaded.')
        return redirect('home')

    context = {'form':form,'page':page,'genres':genres}
    return render(request,'meme/upload_image.html',context)

def homeFilter(request,pk):
    page = 'meme-filter'
    images = imageUpload.objects.filter(genre=pk)
    page = Genre.objects.get(id=pk)
    genres = Genre.objects.all()
    context = {'images':images,'genres':genres,'page':page}
    return render(request,'meme/home.html',context)


def about(request):
    page = 'about'
    context = {'page':page}
    return render(request,'meme/about.html',context)

#---Search
@login_required


def search_view(request):
    query = request.GET.get('q')
    
    if query:
        # Search users and posts using Q objects
        users = User.objects.filter(Q(first_name__icontains=query) | Q(username__icontains=query) )
        posts = Post.objects.filter(Q() | Q(content__icontains=query))
    else:
        # If no query is provided, return an empty result
        users = []
        posts = []
    
    return render(request, 'search_results.html', {'users': users, 'posts': posts})
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ChatRoom, Comment, Message, Post, Profile, imageUpload

class UserRegistrationForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    info = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'bio', 'info', 'phone_number', 'profile_picture')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content', 'image', 'video')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'info', 'phone_number', 'profile_picture')

#chat form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ('name',)

# Memes 
class ImageUploadForm(ModelForm):
    class Meta:
        model = imageUpload
        fields = '__all__'     
        #memes  

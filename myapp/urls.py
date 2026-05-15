"""
URL configuration for chillr_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.home,name='home'),
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('reels/',views.reels,name='reels'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('create-post/',views.create_post,name='create-post'),
    path('create_reels/',views.create_reels,name='create_reels'),
    path('chat_screen/',views.chat_screen,name='chat_screen'),
    path('chat_screen/<int:pk>',views.chat_screen,name='chat_screen'),
    path('send_message/<int:pk>',views.send_message,name='send_message'),
    path('story_viewer/<int:user_id>/',views.story_viewer,name='story_viewer'),
    path('create_story/',views.create_story,name='create_story'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('followers/',views.followers,name='followers'),
    path('following/',views.following,name='following'),
    path('follow_unfollow/<int:pk>',views.follow_unfollow,name='follow_unfollow'),
    path('remove_follower/<int:pk>',views.remove_follower,name='remove_follower'),
    path('follow_back/<int:pk>',views.follow_back,name='follow_back'),
    path('notifications/',views.notifications,name='notifications'),
    path('like_unlike/<int:pk>',views.like_unlike,name='like_unlike'),

    
   
    
]

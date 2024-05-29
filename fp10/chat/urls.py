from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'chat'

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("video/<str:room_name>/", views.video, name="video"),
    path("start_chat/<str:username>/", views.start_chat, name="start_chat"),
    
]

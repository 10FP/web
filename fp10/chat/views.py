from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Room, Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .consumers import OnlineStatusConsumer

Custom_user = get_user_model()
def index(request):
    Custom_user = get_user_model()
    users = Custom_user.objects.all()
    return render(request, "chat/index.html", {"users": users})

def room(request, room_name):
    Custom_user = get_user_model()
    users = Custom_user.objects.all()
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)
    if (request.user != room.first_user) or (request.user != room.second_user):
        redirect("chat:index") 
    return render(request, "chat/room_v2.html", {"room_name": room_name, "room": room, "users": users, "messages": messages})

def start_chat(request, username):
    second_user = Custom_user.objects.get(username = username)
    
    try:
        room = Room.objects.get(first_user = request.user, second_user = second_user)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(first_user = second_user, second_user = request.user)
        except Room.DoesNotExist:
            room = Room.objects.create(first_user = request.user, second_user = second_user)
            
    
    return redirect(f'/chat/{room.id}')

def video(request, room_name):
    room = Room.objects.get(id=room_name)
    if (request.user != room.first_user) or (request.user != room.second_user):
        redirect("chat:index") 
    return render(request, "chat/video_chat.html", {"room": room})

@api_view(['GET'])
def get_user_by_username(request, username):
    Custom_user = get_user_model()
    try:
        user = Custom_user.objects.get(username=username)
       
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            
        })
    except User.DoesNotExist:
        return Response({'message': 'Kullanıcı bulunamadı'}, status=404)
    

@receiver(pre_save, sender=Custom_user)
def check_online_status_change(sender, instance, **kwargs):
    try:
        old_instance = Custom_user.objects.get(pk=instance.pk)
        
        if old_instance.online_status != instance.online_status:
            print("views.py")
            channel_layer = get_channel_layer()
            print(channel_layer)
            async_to_sync(channel_layer.group_send)(
                'online_status_group',
                {
                    'type': 'notify_status_change',
                    'user': instance.username,
                    'online_status': instance.online_status
                }
            )
        
    except Custom_user.DoesNotExist:
       
        pass
        
    
        

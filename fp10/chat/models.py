from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings
# Create your models here.

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='room_first', on_delete=models.CASCADE)
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='room_second', on_delete=models.CASCADE)

class ChatUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chat_user', verbose_name='Kullanıcı', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='chat_users', verbose_name='Oda', on_delete=models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', verbose_name='Kullanıcı', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', verbose_name='Oda', on_delete=models.CASCADE)
    content=models.TextField(verbose_name='Mesaj İçeriği')
    created_date = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=50, null=True)

    def get_short_date(self):
        return str(self.created_date.hour) + ":" + str(self.created_date.minute)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Message, Room, ChatUser

class RoomAdmin(admin.ModelAdmin):
    fields = ["id", "first_user", "second_user"]

class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['created_date']
    fields = ["user", "room", "content", "created_date", "type_of"]

class ChatUserAdmin(admin.ModelAdmin):
    fields = ["user", "room"]


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ChatUser, ChatUserAdmin)

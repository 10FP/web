from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student_card, Activity

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'job', 'is_email_verified', 'last_username_change_date', 'verification_code', "online_status")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'job', 'is_email_verified', 'last_username_change_date', 'verification_code', 'student_number', 'student_department', "online_status")}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'profile_picture', 'job'),
        }),
    )

class StudentCardAdmin(admin.ModelAdmin):
    fields = ["student_card", 'student_owner']

class ActivityAdmin(admin.ModelAdmin):
    fields = ["title", 'text', "picture", 'owner', "partitions"]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student_card, StudentCardAdmin)
admin.site.register(Activity, ActivityAdmin)
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'fp10_app'

urlpatterns = [
    path("", views.index),
    path("login/", views.login),
    path("signup/", views.signup_view, name="signup"),
    path('create-activity/', views.create_activity, name='create_activity'),
    path('join-activity/<int:activity_id>/', views.join_activity, name='join_activity'),
    path("student-card-verification/", views.student_card_verification, name="student_card_verification"),

]

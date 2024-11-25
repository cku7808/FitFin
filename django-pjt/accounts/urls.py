from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('social_login/', views.social_login),
    path('signup_products/', views.signup_products),
    path('userinfo/', views.user_info),
]

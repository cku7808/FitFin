from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('exchangerate/', views.exchangerate),
    path('save-deposit-products/', views.save_deposit_products),
    path('save-saving-products/', views.save_saving_products),
]

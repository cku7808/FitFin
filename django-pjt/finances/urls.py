from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('exchangerate/', views.exchangerate),
    path('save-deposit-products/', views.save_deposit_products),
    path('save-saving-products/', views.save_saving_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-products/<str:product_id>/', views.deposit_products_detail),
    path('saving-products/', views.saving_products),
    path('saving-products/<str:product_id>/', views.saving_products_detail),
]

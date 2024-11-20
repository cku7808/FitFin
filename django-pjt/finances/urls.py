from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('exchangerate/', views.exchangerate),
    path('save-deposit-products/', views.save_deposit_products),
    path('save-saving-products/', views.save_saving_products),
    path('load-deposit-products/', views.load_deposit_products),
    path('load-deposit-products/<str:product_id>/', views.load_deposit_products_detail),
    path('load-saving-products/', views.load_saving_products),
    path('load-saving-products/<str:product_id>/', views.load_saving_products_detail),
]

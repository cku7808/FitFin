from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('product-list/', views.product_list),
    path('product-list/<int:product_id>/', views.product_list_detail),
    path('product-option-list/', views.product_option_list),
    path('product-option-list/<int:product_id>/', views.product_option_list_detail)
]

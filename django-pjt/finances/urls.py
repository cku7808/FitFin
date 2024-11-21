from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('load-today-exchangerate/', views.load_today_exchangerate),
    path('load-exchangerate/', views.load_exchangerate),
    path('save-deposit-products/', views.save_deposit_products),
    path('save-saving-products/', views.save_saving_products),
    
    # 테스트용 url
    path('save-exchangerate/', views.save_exchangerate),
    path('updatetoday-exchangerate/', views.updatetoday_exchangerate),
]

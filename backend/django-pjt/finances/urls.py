from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('load-today-exchangerate/', views.load_today_exchangerate),
    path('load-exchangerate/', views.load_exchangerate),
    path('load-max-exchangerate/', views.load_max_exchangerate),
    path('load-min-exchangerate/', views.load_min_exchangerate),
    path('save-deposit-products/', views.save_deposit_products),
    path('save-saving-products/', views.save_saving_products),
    path('save-laon-products/', views.save_loan_products),
    path('save-laon-total/', views.save_loan_total),
    path('deposit-products/', views.deposit_products),
    path('deposit-products/<str:product_id>/', views.deposit_products_detail),
    path('saving-products/', views.saving_products),
    path('saving-products/<str:product_id>/', views.saving_products_detail),
    path('load-my-products/', views.load_my_products),
    path('recommend-loan-product/', views.recommend_loans),
    
    # 테스트용 url
    path('save-exchangerate/', views.save_exchangerate),
    path('updatetoday-exchangerate/', views.updatetoday_exchangerate),
]

from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list ),
    path('articles/<int:article_pk>/', views.article_detail ),
    
    path('articles/<int:article_pk>/like/', views.like_article ),
    path('articles/<int:article_pk>/comment/', views.comment ),
    path('articles/<int:article_pk>/comment/<int:comment_pk>/', views.comment_edit ),
] 
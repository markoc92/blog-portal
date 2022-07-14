from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('search/', views.post_search, name='post_search'),
    path('create/', views.post_create, name='post_create'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('publish/<int:pk>/', views.post_publish, name='post_publish'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('<int:pk>/', views.post_single, name='post_single'),
    path('category/<str:name>/', views.category, name='category'),
]

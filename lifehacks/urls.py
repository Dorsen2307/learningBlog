from django.urls import path
from . import views

app_name = 'lifehacks'
urlpatterns = [
    path('', views.index, name='index'),
    path('lifehacks/<int:lifehack_id>/', views.lifehack_detail, name='lifehack_detail'),
]
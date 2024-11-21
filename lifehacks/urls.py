from django.urls import path
from . import views

app_name = 'lifehacks'
urlpatterns = [
    path('', views.index, name='index'),
]
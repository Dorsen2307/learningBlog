from django.urls import path
from . import views

app_name = 'poets'
urlpatterns = [
    path('', views.index, name='index'),
]
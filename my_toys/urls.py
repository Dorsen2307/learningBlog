from django.urls import path
from . import views

app_name = 'my_toys'
urlpatterns = [
    path('', views.index, name='index'),
    path('toys/<int:item_id>/', views.toy_detail, name='toy_detail'),
]
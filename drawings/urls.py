from django.urls import path
from . import views

app_name = 'drawings'
urlpatterns = [
    path('', views.index, name='index'),
    path('drawings/<int:drawing_id>/', views.drawing_detail, name='drawing_detail'),
]
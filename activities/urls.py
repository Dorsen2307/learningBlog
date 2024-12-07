from django.urls import path

from . import views

app_name = 'activities'
urlpatterns = [
    path('', views.index, name='index'),
    path('activities/<int:item_id>/', views.activity_detail, name='activities'),
]
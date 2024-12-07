from django.urls import path
from . import views

app_name = 'poets'
urlpatterns = [
    path('', views.index, name='index'),
    path('poets/<int:item_id>/', views.poet_detail, name='poet_detail'),
]
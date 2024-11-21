from django.urls import path
from . import views

app_name = 'crafts'
urlpatterns = [
    path('', views.index, name='index'),
    path('crafts/<int:craft_id>/', views.craft_detail, name='craft_detail'),
]
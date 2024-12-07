from django.urls import path
from . import views

app_name = 'crafts'
urlpatterns = [
    path('', views.index, name='index'),
    path('crafts/<int:item_id>/', views.craft_detail, name='craft_detail'),
]
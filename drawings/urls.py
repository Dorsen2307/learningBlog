from django.urls import path, include
from . import views

app_name = 'drawings'
urlpatterns = [
    path('', views.index, name='index'),
    path('drawings/<int:item_id>/', views.drawing_detail, name='drawing_detail'),
    # path('drawings/<int:item_id>/like/', include('like.urls')),
]
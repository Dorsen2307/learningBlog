from django.urls import path
from .views import like_view

app_name = 'like'
urlpatterns = [
    path('', like_view, name='like_view'),
]
from django.urls import path
from .views import like_object

app_name = 'like'
urlpatterns = [
    path('', like_object, name='like_object'),
]
"""
URL configuration for learningProjectBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='about/', permanent=True)),
    path('about/', include('about.urls')),
    path('my-toys/', include('my_toys.urls')),
    path('drawings/', include('drawings.urls')),
    path('crafts/', include('crafts.urls')),
    path('lifehacks/', include('lifehacks.urls')),
    path('like/<str:app_label>/<str:model_name>/<int:object_id>/', include('like.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
]

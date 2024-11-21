import uuid
from http.client import HTTPResponse

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST

from like.models import Like


@require_POST
def like_object(request, model_name, object_id):
    # Получаем тип контента (модель) по app_label и model_name
    content_type = ContentType.objects.get(model=model_name)
    # Получаем идентификатор пользователя из куки
    user_identifier = request.COOKIES.get('user_identifier')

    # Если куки нет, создаем новый уникальный идентификатор
    if not user_identifier:
        user_identifier = str(uuid.uuid4())
        response = JsonResponse({'likes_count': get_likes_count(content_type, object_id)})
        response.set_cookie('user_identifier', user_identifier, max_age=365*24*60*60) # Устанавливаем куки на 1 год
        return response

    ip_address = request.META.get('REMOTE_ADDR') # Получаем IP-адрес пользователя

    if not Like.objects.filter(
            content_type=content_type,
            object_id=object_id,
            user_identifier=user_identifier,
            ip_address=ip_address).exists():
        Like.objects.create(
            content_type=content_type,
            object_id=object_id,
            user_identifier=user_identifier,
            ip_address=ip_address)
    return JsonResponse({'likes_count': get_likes_count(content_type, object_id)})

def get_likes_count(content_type, object_id):
    return Like.objects.filter(content_type=content_type, object_id=object_id).count()
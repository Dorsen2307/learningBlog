import json
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from like.models import Like


@login_required
@require_POST
def like_object(request):
    data = json.loads(request.body)
    content_type = data.get('content_type')
    object_id = data.get('object_id')

    # Получаем тип контента
    content_type = ContentType.objects.get(model=content_type)
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )

    if created:
        # Лайк был добавлен
        liked = True
    else:
        # Лайк был удален
        like.delete()
        liked = False

    # Получаем количество лайков для данного поста
    like_count = Like.objects.filter(content_type=content_type, object_id=object_id).count()
    print('Like count:', like_count)

    return JsonResponse({'like_count': like_count, 'liked': liked})
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Like

@login_required
@require_POST
def like_view(request):
    content_type = request.POST.get('content_type')
    object_id = request.POST.get('object_id')
    liked = request.POST.get('liked') == 'true'

    try:
        content_type = ContentType.objects.get(model=content_type)
    except ContentType.DoesNotExist:
        return JsonResponse({'error': 'Content type not found'}, status=400)

    # Проверяем, лайк уже существует
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id
    )

    # Если можно поставить лайк
    if liked:
        # Если лайк создали, удаляем его
        if not created:
            like.delete()
            liked = 'false'
        else:
            liked = 'true'
    else:
        # Если лайка нет, создаем его
        if created:
            liked = 'false'
        else:
            liked = 'true'
            like.delete()

    # Получаем новое количество лайков
    like_count = Like.objects.filter(content_type=content_type, object_id=object_id).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

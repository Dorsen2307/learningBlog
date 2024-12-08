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

    if liked:
        # Если лайк уже существует, удаляем его
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
    else:
        # Если лайка нет, создаем его
        if created:
            liked = False
        else:
            liked = True
            like.delete()

    # Получаем новое количество лайков
    like_count = Like.objects.filter(content_type=content_type, object_id=object_id).count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

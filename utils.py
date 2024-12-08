from datetime import timedelta

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Case, When, BooleanField
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from activities.models import Activities
from comments.forms import CommentForm
from crafts.models import Crafts
from drawings.models import Drawings
from lifehacks.models import Lifehacks
from like.models import Like
from my_toys.models import MyToys
from poets.models import Poets

model_mapping = {
        'drawing' : Drawings,
        'activity' : Activities,
        'craft' : Crafts,
        'poet' : Poets,
        'lifehack' : Lifehacks,
        'toy' : MyToys,
    }

def handle_comment(request, form, instance):
    '''Обработка и привязка комментария к посту'''
    if form.is_valid():
        comment = form.save(commit=False)

        if isinstance(instance, Drawings):
            comment.drawing = instance
        elif isinstance(instance, Activities):
            comment.activity = instance
        elif isinstance(instance, Crafts):
            comment.craft = instance
        elif isinstance(instance, Poets):
            comment.poet = instance
        elif isinstance(instance, Lifehacks):
            comment.lifehack = instance
        elif isinstance(instance, MyToys):
            comment.my_toy = instance

        if request.user.is_authenticated:
            comment.name = request.user.username
        else:
            comment.name = form.cleaned_data['name']

        comment.is_approved = False
        comment.save()
        messages.info(request, 'Ваш комментарий находится на модерации.')
        return True
    return False

def index_view(request, item_type, template_name):
    today = timezone.now()
    model = model_mapping.get(item_type)

    item_list = model.objects.filter(is_published=True).annotate(
        is_recent=Case(
            When(date_published__gte=today - timedelta(days=5), then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).order_by('-is_recent', '-date_published')

    context = {'item_list' : item_list}
    return render(request, template_name, context)

def detail_view(request, item_id, item_type, template_name):
    '''Общая функция вывода детальной информации с комментариями'''
    url_mapping = {
        'drawing' : 'drawings:drawing_detail',
        'activity' : 'activities:activity_detail',
        'craft' : 'crafts:craft_detail',
        'poet' : 'poets:poet_detail',
        'lifehack' : 'lifehacks:lifehack_detail',
        'toy' : 'my_toys:toy_detail',
    }

    model = model_mapping.get(item_type)
    if model is None:
        raise ValueError("Недопустимый тип элемента")

    item = get_object_or_404(model, id=item_id)
    comments = item.comments.filter(is_approved=True).order_by('-created_at')

    # Получаем количество лайков для данного объекта
    content_type = ContentType.objects.get_for_model(item)
    like_count = Like.objects.filter(content_type=content_type, object_id=item.id).count()

    if request.method == 'POST':
        form = CommentForm(request.POST, user_authenticated=request.user.is_authenticated)
        if handle_comment(request, form, item):
            url_name = url_mapping.get(item_type)
            return redirect(url_name, item_id=item.id)
    else:
        form = CommentForm(user_authenticated=request.user.is_authenticated)

    context = {
        'item': item,
        'comments': comments,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'like_count': like_count,
    }

    return render(request, template_name, context)
from datetime import timedelta
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Case, When, BooleanField, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
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
        'drawings' : Drawings,
        'activities' : Activities,
        'crafts' : Crafts,
        'poets' : Poets,
        'lifehacks' : Lifehacks,
        'mytoys' : MyToys,
    }
PAGE_COUNT = 10 # Кол-во постов на странице в комментариях

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

    # Получаем количество лайков и статус для каждого элемента
    for item in item_list:
        content_type = ContentType.objects.get_for_model(item)
        if request.user.is_authenticated:
            like = Like.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=item.id,
            ).first()

            item.like_count = Like.objects.filter(content_type=content_type, object_id=item.id).count()
            item.liked = 'false' if like else 'true'
        else:
            item.like_count = 0
            item.liked = None

    context = {'item_list' : item_list}

    return render(request, template_name, context)

def detail_view(request, item_id, item_type, template_name):
    '''Общая функция вывода детальной информации с комментариями'''
    url_mapping = {
        'drawings' : 'drawings:drawing_detail',
        'activities' : 'activities:activity_detail',
        'crafts' : 'crafts:craft_detail',
        'poets' : 'poets:poet_detail',
        'lifehacks' : 'lifehacks:lifehack_detail',
        'mytoys' : 'my_toys:toy_detail',
    }

    model = model_mapping.get(item_type)
    if model is None:
        raise ValueError("Недопустимый тип элемента")

    item = get_object_or_404(model, id=item_id)
    comments_list = item.comments.filter(is_approved=True).order_by('-created_at')

    # # Настройка пагинации
    paginator = Paginator(comments_list, PAGE_COUNT)
    page_number = request.GET.get('page', 1)
    is_admin = request.user.is_staff
    print(is_admin)

    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return load_comments(request, item_id, item_type)

    if request.method == 'POST':
        form = CommentForm(request.POST, user_authenticated=request.user.is_authenticated)
        if handle_comment(request, form, item):
            url_name = url_mapping.get(item_type)
            return redirect(url_name, item_id=item.id)
    else:
        form = CommentForm(user_authenticated=request.user.is_authenticated)

    # Получаем количество лайков и статус для данного объекта
    content_type = ContentType.objects.get_for_model(item)
    if request.user.is_authenticated:
        like = Like.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=item.id,
        ).first()

        like_count = Like.objects.filter(content_type=content_type, object_id=item.id).count()
        if like:
            liked = 'false'
        else:
            liked = 'true'
    else:
        liked = None
        like_count = 0

    context = {
        'item': item,
        'item_id': item.id,
        'item_type': item_type,
        'comments': comments,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'like_count': like_count,
        'liked': liked,
        'is_admin': is_admin,
    }

    return render(request, template_name, context)

def load_comments(request, item_id, item_type):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        model = model_mapping.get(item_type)
        item = get_object_or_404(model, id=item_id)
        comments_list = item.comments.filter(is_approved=True).order_by('-created_at')
        paginator = Paginator(comments_list, PAGE_COUNT)  # Показывать PAGE_COUNT комментариев на странице

        page_number = request.GET.get('page')
        comments = paginator.get_page(page_number)

        comments_html = render_to_string('comments/comments_partial.html', {'comments': comments})
        paginator_html = render_to_string('comments/comments_paginator.html', {
            'comments': comments,
            'item_id': item.id,
            'item_type': item_type,
        })

        return JsonResponse({
            'comments_html': comments_html,
            'paginator_html': paginator_html,
            'has_previous': comments.has_previous(),
            'has_next': comments.has_next(),
            'current_page': comments.number,
            'total_pages': comments.paginator.num_pages,
        })
    else:
        return JsonResponse({'error' : 'Invalid request'}, status=400)
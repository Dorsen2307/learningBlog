import os
from datetime import timedelta
from django.conf import settings
from PIL import Image
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Case, When, BooleanField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from activities.models import Activities
from comments.forms import CommentForm
from crafts.models import Crafts
from displaying_sections.models import Section
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
PAGE_COUNT = 3 # Кол-во постов на странице в комментариях

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
    '''Функция вывода контента соответствующего раздела'''
    today = timezone.now()
    model = model_mapping.get(item_type)
    sections_list = get_section()

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

    context = {
        'item_list' : item_list,
        'sections_list' : sections_list,
	    'MEDIA_URL' : settings.MEDIA_URL,
    }

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
    sections_list = get_section()
    admins = User.objects.filter(is_staff=True)

    model = model_mapping.get(item_type)
    if model is None:
        raise ValueError("Недопустимый тип элемента")

    item = get_object_or_404(model, id=item_id)
    comments_list = item.comments.filter(is_approved=True).order_by('-created_at')

    # if item.image and item.image.image:
    #     # Путь к оригинальному изображению
    #     original_image_path = item.image.image.path
    #     logo_path = 'static/img/logo-watermark.png'
    #     output_image_path = f'static/img/content/watermark/watermarked_{item_type}_{item.id}.jpg'
    #
    #     # Добавляем водяной знак
    #     if not os.path.exists(output_image_path):
    #         add_watermark(original_image_path, logo_path, output_image_path)

    # Настройка пагинации
    paginator = Paginator(comments_list, PAGE_COUNT)
    page_number = request.GET.get('page', 1)

    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    for comment in comments:
        for admin in admins:
            if comment.name == admin.username:
                comment.is_admin = True
                break

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

    # if item.image and item.image.image:
    #     context = {
    #         'item': item,
    #         'watermarked_image': f'/{output_image_path}',
    #         'item_id': item.id,
    #         'item_type': item_type,
    #         'comments': comments,
    #         'form': form,
    #         'is_authenticated': request.user.is_authenticated,
    #         'like_count': like_count,
    #         'liked': liked,
    #         'is_admin': is_admin,
    #         'sections_list': sections_list,
    #     }
    # else:
    context = {
        'item': item,
        'item_id': item.id,
        'item_type': item_type,
        'comments': comments,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'like_count': like_count,
        'liked': liked,
        'sections_list': sections_list,
	    'MEDIA_URL' : settings.MEDIA_URL,
    }




    return render(request, template_name, context)

def load_comments(request, item_id, item_type):
    '''Загружает комментарии и пагинацию'''
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        model = model_mapping.get(item_type)
        item = get_object_or_404(model, id=item_id)
        admins = User.objects.filter(is_staff=True)
        comments_list = item.comments.filter(is_approved=True).order_by('-created_at')
        paginator = Paginator(comments_list, PAGE_COUNT)  # Показывать PAGE_COUNT комментариев на странице

        page_number = request.GET.get('page')
        comments = paginator.get_page(page_number)

        for comment in comments:
            for admin in admins:
                if comment.name == admin.username:
                    comment.is_admin = True
                    break

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

def add_watermark(original_image_path, logo_path, output_image_path, position=(0, 0), transparency=128):
    '''Функция накладывает водяной знак на оригинальное изображение и сохраняет'''
    # Открываем оригинальное изображение
    original = Image.open(original_image_path).convert("RGBA")

    # Открываем изображение логотипа
    logo = Image.open(logo_path).convert("RGBA")

    # Изменяем размер логотипа, если необходимо
    logo_size = (
    int(original.size[0] * 0.2), int(original.size[1] * 0.12))
    logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

    # Создаем изображение для водяного знака
    watermark = Image.new("RGBA", original.size)

    # Определяем позицию для логотипа
    logo_position = (
    original.size[0] - logo.size[0] - 50, original.size[1] - logo.size[1] - 50)  # Низкий правый угол с отступом

    # Накладываем логотип на водяной знак с заданной прозрачностью
    watermark.paste(logo, logo_position, logo)

    # Объединяем оригинал и водяной знак
    combined = Image.alpha_composite(original, watermark)

    # Создание директории, если не существует
    output_dir = os.path.dirname(output_image_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Сохраняем результат
    combined.convert("RGB").save(output_image_path, "JPEG")

def get_section():
    sections_list = Section.objects.filter(is_active=True)

    return sections_list
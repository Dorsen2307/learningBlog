from datetime import timedelta

from django.contrib import messages
from django.db.models import Case, When, BooleanField
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from comments.forms import CommentForm
from .models import Lifehacks

def index(request):
    today = timezone.now()

    lifehacks_list = Lifehacks.objects.filter(is_published=True).annotate(
        is_recent=Case(
            When(date_published__gte=today - timedelta(days=5), then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).order_by('-is_recent', '-date_published')

    context = {'lifehacks_list' : lifehacks_list}
    return render(request, 'creativity/lifehacks/index.html', context)

def lifehack_detail(request, lifehack_id):
    lifehacks = get_object_or_404(Lifehacks, id=lifehack_id)
    comments = lifehacks.comments.filter(is_approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lifehack = lifehacks
            comment.is_approved = False
            comment.save()
            messages.info(request, 'Ваш комментарий находится на модерации.')
            return redirect('lifehacks:lifehack_detail', lifehack_id=lifehacks.id)
    else:
        form = CommentForm()

    context = {
        'lifehacks': lifehacks,
        'comments': comments,
        'form': form,
    }

    return render(request, 'creativity/lifehacks/lifehack.html', context)
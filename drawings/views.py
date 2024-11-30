from datetime import timedelta
from django.db.models import Case, When, BooleanField
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages
from comments.forms import CommentForm
from .models import Drawings
from django.contrib import messages

def index(request):
    today = timezone.now()

    drawings_list = Drawings.objects.filter(is_published=True).annotate(
        is_recent=Case(
            When(date_published__gte=today - timedelta(days=5), then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).order_by('-is_recent', '-date_published')

    context = {'drawings_list' : drawings_list}
    return render(request, 'creativity/drawings/index.html', context)

def drawing_detail(request, drawing_id):
    drawings = get_object_or_404(Drawings, id=drawing_id)
    comments = drawings.comments.filter(is_approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.drawing = drawings
            comment.is_approved = False
            comment.save()
            messages.info(request, 'Ваш комментарий находится на модерации.')
            return redirect('drawings:drawing_detail', drawing_id=drawings.id)
    else:
        form = CommentForm()

    context = {
        'drawings': drawings,
        'comments': comments,
        'form': form,
    }

    return render(request, 'creativity/drawings/drawing.html', context)
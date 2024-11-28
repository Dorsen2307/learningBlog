from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from comments.forms import CommentForm
from .models import Drawings

def index(request):
    drawings_list = Drawings.objects.filter(is_published=True).order_by('-date_painting')
    today = timezone.now()

    for drawing in drawings_list:
        drawing.is_recent = (today.date() - drawing.date_published) < timedelta(days=5)

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
            comment.save()
            return redirect('drawings:drawing_detail', drawings_id=drawings.id)
    else:
        form = CommentForm()

    context = {'drawings': drawings, 'comments': comments, 'form': form}

    return render(request, 'creativity/drawings/drawing.html', context)
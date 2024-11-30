from datetime import timedelta

from django.contrib import messages
from django.db.models import Case, When, BooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from .models import MyToys

def index(request):
    today = timezone.now()

    my_toys_list = MyToys.objects.filter(is_published=True).annotate(
        is_recent=Case(
            When(date_published__gte=today - timedelta(days=5), then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).order_by('-is_recent', '-date_published')

    context = {'my_toys_list' : my_toys_list}
    return render(request, 'mytoys/index.html', context)

def toy_detail(request, toy_id):
    my_toys = get_object_or_404(MyToys, id=toy_id)
    comments = my_toys.comments.filter(is_approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.my_toy = my_toys
            comment.is_approved = False
            comment.save()
            messages.info(request, 'Ваш комментарий находится на модерации.')
            return redirect('my_toys:toy_detail', toy_id=my_toys.id)
    else:
        form = CommentForm()

    context = {
        'my_toys': my_toys,
        'comments': comments,
        'form': form,
    }

    return render(request, 'mytoys/toys.html', context)
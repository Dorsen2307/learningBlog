from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from .models import MyToys

def index(request):
    my_toys_list = MyToys.objects.filter(is_published=True)
    today = timezone.now()

    for toys in my_toys_list:
        toys.is_recent = (today.date() - toys.date_published) < timedelta(days=5)

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
            comment.save()
            return redirect('my_toys:toy_detail', toy_id=my_toys.id)
    else:
        form = CommentForm()

    context = {'my_toys': my_toys, 'comments': comments, 'form': form,}

    return render(request, 'mytoys/toys.html', context)
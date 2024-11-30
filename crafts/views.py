from datetime import timedelta
from time import timezone

from django.contrib import messages
from django.db.models import Case, When, BooleanField
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from comments.forms import CommentForm
from .models import Crafts

def index(request):
    today = timezone.now()

    crafts_list = Crafts.objects.filter(is_published=True).annotate(
        is_recent=Case(
            When(date_published__gte=today - timedelta(days=5), then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).order_by('-is_recent', '-date_published')

    context = {'crafts_list' : crafts_list}
    return render(request, 'creativity/crafts/index.html', context)

def craft_detail(request, craft_id):
    crafts = get_object_or_404(Crafts, id=craft_id)
    comments = crafts.comments.filter(is_approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.craft = crafts
            comment.is_approved = False
            comment.save()
            messages.info(request, 'Ваш комментарий находится на модерации.')
            return redirect('crafts:craft_detail', craft_id=crafts.id)
    else:
        form = CommentForm()

    context = {
        'crafts': crafts,
        'comments': comments,
        'form': form,
    }

    return render(request, 'creativity/crafts/craft.html', context)
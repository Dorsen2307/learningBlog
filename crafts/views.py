from django.shortcuts import render, get_object_or_404, redirect

from comments.forms import CommentForm
from .models import Crafts

def index(request):
    crafts_list = Crafts.objects.filter(is_published=True)
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
            comment.save()
            return redirect('crafts:craft_detail', toy_id=crafts.id)
    else:
        form = CommentForm()

    context = {'crafts': crafts, 'comments': comments, 'form': form,}

    return render(request, 'creativity/crafts/craft.html', context)
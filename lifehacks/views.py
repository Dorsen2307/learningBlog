from django.shortcuts import render, get_object_or_404, redirect
from comments.forms import CommentForm
from .models import Lifehacks

def index(request):
    lifehacks_list = Lifehacks.objects.filter(is_published=True)
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
            comment.save()
            return redirect('lifehacks:lifehack_detail', toy_id=lifehacks.id)
    else:
        form = CommentForm()

    context = {'lifehacks': lifehacks, 'comments': comments, 'form': form,}

    return render(request, 'creativity/lifehacks/lifehack.html', context)
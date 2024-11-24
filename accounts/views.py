from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import SignUpForm, LoginForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('about:index')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
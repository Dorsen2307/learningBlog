from django.shortcuts import render
from .models import About


def index(request):
    about = About.objects.filter(is_active=True)

    if about:
        image_url = about.image.image.url if about.image else ''
        context = {'photo' : image_url, 'content' : about.text}
    else:
        context = {'content' : 'Этот раздел пока в разработке!'}

    return render(request,
                  'about/index.html',
                  context)



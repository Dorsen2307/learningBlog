from django.shortcuts import render
from django.conf import settings
from utils import get_section
from .models import About


def index(request):
    about = About.objects.get(is_active=True)

    if about:
        image_url = about.image.image.url if about.image else ''
        sections_list = get_section()
        context = {'photo' : image_url, 'content' : about.content, 'sections_list' : sections_list, 'MEDIA_URL' : settings.MEDIA_URL,}
    else:
        context = {'content' : 'Этот раздел пока в разработке!'}

    return render(request,
                  'about/index.html',
                  context)



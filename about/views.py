from django.shortcuts import render
from django.conf import settings
from utils import get_section, get_info
from .models import About


def index(request):
    about = About.objects.get(is_active=True)

    if about:
        image_url = about.image.image.url if about.image else ''
        sections_list = get_section()
        info_list = get_info()
        context = {
            'photo' : image_url,
            'content' : about.content,
            'sections_list' : sections_list,
            'info_list' : info_list,
            'MEDIA_URL' : settings.MEDIA_URL,
        }
    else:
        context = {'content' : 'Этот раздел пока в разработке!'}

    return render(request,
                  'about/index.html',
                  context)



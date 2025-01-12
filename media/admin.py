import os

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('category', 'image_filename', 'image_preview')
    readonly_fields = ('image_preview',)
    # actions = ['delete_model']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            filename = obj.image.name
            absolute_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, filename))
            # print(absolute_path)
            # print(filename)
            if os.path.isfile(absolute_path):
                os.remove(absolute_path)
            # obj.delete()
        return super().delete_queryset(request, queryset)

    def image_filename(self, obj):
        return obj.image.name.split('/')[-1]
    image_filename.short_description = 'Имя файла'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px;">', obj.image.url)
        return 'Фото отсутствует'
    image_preview.short_description = 'Предпросмотр'

admin.site.register(Image, ImageAdmin)
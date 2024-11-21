from django.contrib import admin
from django.utils.html import format_html
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('category', 'image_filename', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_filename(self, obj):
        return obj.image.name.split('/')[-1]
    image_filename.short_description = 'Имя файла'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px;">', obj.image.url)
        return 'Фото отсутствует'
    image_preview.short_description = 'Предпросмотр'

admin.site.register(Image, ImageAdmin)
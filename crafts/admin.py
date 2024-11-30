from django.contrib import admin
from django.utils.html import format_html
from media.models import Image
from .models import Crafts


class CraftsAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'text_preview',
                    'image_preview_list',
                    'date_crafting',
                    'date_created',
                    'date_published',
                    'is_published'
    )
    list_editable = ('is_published',)
    ordering = ('name',)
    fields = ('image',
              'name',
              'content',
              'is_published',
              'date_crafting',
              'image_preview',
    )
    readonly_fields = ('image_preview', 'image_preview_list',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.is_relation and db_field.related_model == Image:
            category_filter = 'crafts'
            kwargs['queryset'] = Image.objects.filter(category=category_filter)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def text_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    text_preview.short_description = 'Текст'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px;">', obj.image.image.url)
        return 'Фото отсутствует'
    image_preview.short_description = 'Изображения'

    def image_preview_list(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 50px;">', obj.image.image.url)
        return 'Фото отсутствует'
    image_preview.short_description = 'Изображения'

admin.site.register(Crafts, CraftsAdmin)

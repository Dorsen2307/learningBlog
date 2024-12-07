from django.contrib import admin
from .models import Comment

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('get_related_object', 'name', 'content_views', 'created_at', 'is_approved',)
    fields = ('name', 'content', 'is_approved',)

    def get_related_object(self, obj):
        related_object = None
        if obj.my_toy:
            related_object = f'Моя игрушка: {obj.my_toy}'
        elif obj.drawing:
            related_object = f'Рисунок: {obj.drawing}'
        elif obj.craft:
            related_object = f'Поделка: {obj.craft}'
        elif obj.lifehack:
            related_object = f'Хитрость: {obj.lifehack}'
        elif obj.activity:
            related_object = f'Активность: {obj.activity}'
        elif obj.poet:
            related_object = f'Стих: {obj.poet}'

        return related_object or '-'

    get_related_object.short_description = 'Объект'

    def content_views(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_views.short_description = 'Текст'

admin.site.register(Comment, CommentsAdmin)

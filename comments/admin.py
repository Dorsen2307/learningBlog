from django.contrib import admin
from .models import Comment

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('get_related_object', 'name', 'content_views', 'created_at', 'is_approved',)
    fields = ('name', 'content', 'is_approved',)

    def get_related_object(self, obj):
        if obj.my_toy:
            return f'Моя игрушка: {obj.my_toy}'
        elif obj.drawing:
            return f'Рисунок: {obj.drawing}'
        elif obj.craft:
            return f'Поделка: {obj.craft}'
        elif obj.lifehack:
            return f'Хитрость: {obj.lifehack}'
        elif obj.activity:
            return f'Активность: {obj.activity}'
        elif obj.poet:
            return f'Стих: {obj.poet}'
        return None

    get_related_object.short_description = 'Объект'

    def content_views(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_views.short_description = 'Текст'

admin.site.register(Comment, CommentsAdmin)

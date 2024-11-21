from django.contrib import admin
from .models import Comment

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('my_toy', 'name', 'content_views', 'created_at', 'is_approved',)
    fields = ('name', 'content', 'is_approved',)

    def content_views(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_views.short_description = 'Текст'

admin.site.register(Comment, CommentsAdmin)

from django.contrib import admin

from like.models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'content_type',
        'object_id',
        'created_at'
    )

    ordering = ('created_at',)

    fields = (
        'user',
        'content_type',
        'object_id',
        'created_at'
    )

    readonly_fields = ('created_at',)

admin.site.register(Like, LikeAdmin)
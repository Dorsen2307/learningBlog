from django.contrib import admin
from .models import Info

class InfoAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'date_created',
        'is_published',
    )
    list_editable = ('is_published',)
    ordering = ('date_created',)
    fields = (
        'name',
        'text',
        'is_published',
    )

admin.site.register(Info, InfoAdmin)
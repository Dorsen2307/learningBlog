from django.contrib import admin
from django.db.models import Q

from .models import About, Image


class AboutAdmin(admin.ModelAdmin):
    list_display = ('data_creat', 'is_active', 'text_preview')
    list_editable = ('is_active',)
    fields = ('image', 'content', 'is_active')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.is_relation and db_field.related_model == Image:
            category_filter = 'about'
            kwargs['queryset'] = Image.objects.filter(category=category_filter)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def data_creat(self, obj):
        return obj.data_created.strftime('%d.%m.%Y')
    data_creat.short_description = 'Дата создания'

    def text_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    text_preview.short_description = 'Предпросмотр'

    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = "Активно?"

    def save_model(self, request, obj, form, change):
        #Деактивация остальных объектов при сохранении
        if obj.is_active:
            About.objects.filter(~Q(id=obj.id)).update(is_active=False)
        obj.save()

admin.site.register(About, AboutAdmin)



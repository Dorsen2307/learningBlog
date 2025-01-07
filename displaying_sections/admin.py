from django.contrib import admin
from displaying_sections.models import Section


class SectionAdmin(admin.ModelAdmin):
    fields = ('name_section', 'type_section', 'url_section', 'is_active')
    list_display = ('name_section', 'is_active')
    list_editable = ('is_active',)

admin.site.register(Section, SectionAdmin)
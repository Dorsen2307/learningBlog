from django.db import models
from django.urls import reverse


class Section(models.Model):
    type_section = models.CharField(max_length=100, verbose_name='Тип раздела')
    name_section = models.CharField(max_length=100, verbose_name='Имя раздела')
    url_section = models.CharField(max_length=100, verbose_name='Ссылка')
    is_active = models.BooleanField(default=False, verbose_name='Активно?')

    def __str__(self):
        return self.name_section

    def get_url(self):
        return reverse (self.url_section)

    class Meta:
        verbose_name_plural = 'Разделы'
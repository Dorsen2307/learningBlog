from ckeditor.fields import RichTextField
from django.db import models

class Info(models.Model):
    name = models.CharField(max_length=100, verbose_name='О чём информация')
    text = RichTextField(verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано?')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Информация'
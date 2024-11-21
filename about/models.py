from django.db import models
from media.models import Image


class About(models.Model):
    data_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    is_active = models.BooleanField(default=False, verbose_name='Активно?')

    def __str__(self):
        return str(self.data_created.date())

    class Meta:
        verbose_name_plural = 'Моя страничка'


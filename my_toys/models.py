from django.db import models
from django.utils import timezone
from media.models import Image


class MyToys(models.Model):
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Изображение')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано?')
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')
    date_published = models.DateField(null=True, blank=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.name if self.name else 'неизвестный'

    def save(self, *args, **kwargs):
        if self.is_published:
            self.date_published = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Игрушки'
import os
import logging
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

class Image(models.Model):
    CATEGORY = [
        ('about', 'Обо мне'),
        ('mytoys', 'Мои игрушки'),
        ('drawings', 'Рисунки'),
        ('crafts', 'Поделки'),
        ('lifehacks', 'Lifehacks'),
        ('activities', 'Активности'),
        ('poets', 'Поэт'),
    ]

    def get_upload_to(self, filename):
        return f'content/{self.category}/{filename}'

    category = models.CharField(max_length=10, choices=CATEGORY, verbose_name='Категория')
    image = models.ImageField(upload_to=get_upload_to, verbose_name='Изображение')

    def __str__(self):
        return self.image.name.split('/')[-1]

    class Meta:
        verbose_name_plural = 'Изображения'


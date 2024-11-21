from django.db import models


class Image(models.Model):
    CATEGORY = [
        ('about', 'Обо мне'),
        ('mytoys', 'Мои игрушки'),
        ('drawings', 'Рисунки'),
        ('crafts', 'Поделки'),
        ('lifehacks', 'Lifehacks'),
        ('activity', 'Активности'),
        ('poet', 'Поэт'),
    ]

    def get_upload_to(self, filename):
        return f'static/img/content/{self.category}/{filename}'

    category = models.CharField(max_length=10, choices=CATEGORY, verbose_name='Категория')
    image = models.ImageField(upload_to=get_upload_to, verbose_name='Изображение')

    def __str__(self):
        return self.image.name.split('/')[-1]

    class Meta:
        verbose_name_plural = 'Изображения'

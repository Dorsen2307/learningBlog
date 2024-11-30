from django.db import models

from poets.models import Poets
from activities.models import Activities
from lifehacks.models import Lifehacks
from crafts.models import Crafts
from drawings.models import Drawings
from my_toys.models import MyToys


class Comment(models.Model):
    my_toy = models.ForeignKey(MyToys, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    drawing = models.ForeignKey(Drawings, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    craft = models.ForeignKey(Crafts, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    lifehack = models.ForeignKey(Lifehacks, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    poet = models.ForeignKey(Poets, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Создан')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрено?')

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name_plural = 'Комментарии'
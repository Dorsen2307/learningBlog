# Generated by Django 4.2.16 on 2024-12-25 16:25

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crafts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Текст')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликовано?')),
                ('date_crafting', models.DateField(blank=True, null=True, verbose_name='Дата изготовления')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('date_published', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.image', verbose_name='Изображение')),
            ],
            options={
                'verbose_name_plural': 'Поделки',
            },
        ),
    ]

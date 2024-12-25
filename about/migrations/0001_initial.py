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
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Текст')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активно?')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.image', verbose_name='Изображение')),
            ],
            options={
                'verbose_name_plural': 'Моя страничка',
            },
        ),
    ]

# Generated by Django 4.2.16 on 2024-11-16 13:11

from django.db import migrations, models
import media.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('about', 'Обо мне'), ('mytoys', 'Мои игрушки'), ('drawings', 'Рисунки'), ('crafts', 'Поделки'), ('lifehacks', 'Lifehacks'), ('activity', 'Активности'), ('poet', 'Поэт')], max_length=10, verbose_name='Категория')),
                ('image', models.ImageField(upload_to=media.models.Image.get_upload_to, verbose_name='Изображение')),
            ],
            options={
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]

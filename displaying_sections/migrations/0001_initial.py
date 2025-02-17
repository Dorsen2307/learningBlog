# Generated by Django 4.2.16 on 2024-12-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_section', models.CharField(max_length=100, verbose_name='Тип раздела')),
                ('name_section', models.CharField(max_length=100, verbose_name='Имя раздела')),
                ('url_section', models.CharField(max_length=100, verbose_name='Ссылка')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активно?')),
            ],
            options={
                'verbose_name_plural': 'Разделы',
            },
        ),
    ]

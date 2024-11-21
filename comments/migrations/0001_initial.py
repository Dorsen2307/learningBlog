# Generated by Django 4.2.16 on 2024-11-16 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_toys', '0001_initial'),
        ('drawings', '0001_initial'),
        ('crafts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('content', models.TextField(verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Одобрено?')),
                ('crafts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='crafts.crafts')),
                ('drawing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='drawings.drawings')),
                ('my_toy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='my_toys.mytoys')),
            ],
            options={
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]

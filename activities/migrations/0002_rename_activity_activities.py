# Generated by Django 4.2.16 on 2024-11-28 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_activities'),
        ('media', '0001_initial'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Activity',
            new_name='Activities',
        ),
    ]

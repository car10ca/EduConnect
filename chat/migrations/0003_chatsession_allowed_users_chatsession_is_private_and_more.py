# Generated by Django 5.1 on 2024-08-24 23:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatsession_name_chatsession_participants_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsession',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='allowed_chat_sessions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatsession',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chatsession',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='chat_sessions', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 5.1 on 2024-08-25 22:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_chataccessattempt'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chataccessattempt',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Chat Access Attempt', 'verbose_name_plural': 'Chat Access Attempts'},
        ),
        migrations.AlterModelOptions(
            name='chatsession',
            options={'ordering': ['-created_at'], 'verbose_name': 'Chat Session', 'verbose_name_plural': 'Chat Sessions'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['timestamp'], 'verbose_name': 'Message', 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterField(
            model_name='chatsession',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddIndex(
            model_name='chataccessattempt',
            index=models.Index(fields=['user', 'room_name', 'timestamp'], name='chat_chatac_user_id_844c26_idx'),
        ),
    ]

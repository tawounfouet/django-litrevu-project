# Generated by Django 4.2.6 on 2023-10-18 17:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_alter_user_profile_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="subscribers",
            field=models.ManyToManyField(
                blank=True, to=settings.AUTH_USER_MODEL, verbose_name="abonnés"
            ),
        ),
    ]
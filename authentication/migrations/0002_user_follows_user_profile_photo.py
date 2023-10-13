# Generated by Django 4.2.6 on 2023-10-13 20:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="follows",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL, verbose_name="suit"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_photo",
            field=models.ImageField(
                default="default.jpg", upload_to="", verbose_name="photo de profil"
            ),
            preserve_default=False,
        ),
    ]

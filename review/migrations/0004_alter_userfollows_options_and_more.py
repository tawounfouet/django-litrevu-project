# Generated by Django 4.2.6 on 2023-10-19 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("review", "0003_alter_ticket_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userfollows",
            options={
                "verbose_name": "abonnement",
                "verbose_name_plural": "abonnements",
            },
        ),
        migrations.AlterField(
            model_name="userfollows",
            name="followed_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followerd_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
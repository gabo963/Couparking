# Generated by Django 3.2.5 on 2022-12-09 03:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coupark', '0002_auto_20221201_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingreservation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

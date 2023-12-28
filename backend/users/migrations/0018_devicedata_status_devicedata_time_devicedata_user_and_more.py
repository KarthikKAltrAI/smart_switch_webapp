# Generated by Django 5.0 on 2023-12-27 04:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_devicedata_device_remove_devicedata_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicedata',
            name='status',
            field=models.IntegerField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='devicedata',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='devicedata',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]

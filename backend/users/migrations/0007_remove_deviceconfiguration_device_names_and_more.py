# Generated by Django 4.2.7 on 2023-12-07 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_device_name_deviceconfiguration_device_names'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceconfiguration',
            name='device_names',
        ),
        migrations.AlterField(
            model_name='deviceconfiguration',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.device'),
        ),
    ]
# Generated by Django 5.0 on 2023-12-27 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_devicedata_status_devicedata_time_devicedata_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedata',
            name='status',
            field=models.IntegerField(max_length=2),
        ),
    ]

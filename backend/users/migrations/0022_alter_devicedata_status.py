# Generated by Django 5.0 on 2023-12-27 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_devicedata_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedata',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]

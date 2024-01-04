# Generated by Django 4.2.8 on 2024-01-04 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_userprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_ip', models.GenericIPAddressField()),
                ('scheduled_time', models.DateTimeField()),
                ('status', models.CharField(max_length=3)),
                ('processed', models.BooleanField(default=False)),
            ],
        ),
    ]

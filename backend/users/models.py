from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone




# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    username=None

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]


class House(models.Model):
    name=models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Room(models.Model):
    name=models.CharField(max_length=255)
    house=models.ForeignKey(House,on_delete=models.CASCADE)


class Device(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) 
    

class DeviceConfiguration(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17)
    device_password = models.CharField(max_length=255)
    network_ssid = models.CharField(max_length=255)
    network_password = models.CharField(max_length=255)
    
    # Additional fields
    device_name = models.CharField(max_length=255) 
    ip = models.GenericIPAddressField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    voltage = models.FloatField(null=True, blank=True)
    current = models.FloatField(null=True, blank=True)
    power = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
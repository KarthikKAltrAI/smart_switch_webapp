from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save



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
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17)  # Assuming MAC address is in the format 'xx:xx:xx:xx:xx:xx'
    device_password = models.CharField(max_length=255)
    network_ssid = models.CharField(max_length=255)
    network_password = models.CharField(max_length=255)    
   

    


 

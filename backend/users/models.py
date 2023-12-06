from django.db import models
from django.contrib.auth.models import AbstractUser

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

    


 

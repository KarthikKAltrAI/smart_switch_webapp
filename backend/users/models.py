from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager, PermissionsMixin,AbstractBaseUser,Group, Permission
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone



    
class SuperAdmin(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    role=models.CharField(default='SUPERADMIN')

    join_date=models.DateField(default=timezone.now)
    join_time=models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    

class Admin(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    role=models.CharField(default='ADMIN')

    

    join_datetime = models.DateTimeField(default=timezone.now)

    super_admin=models.ForeignKey(SuperAdmin,on_delete=models.CASCADE)

    def __str__(self) :
        return self.name



class Installer(models.Model):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    users=models.IntegerField(null=True)
    join_datetime = models.DateTimeField(default=timezone.now)

    
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    



# Create your models here.
class User(AbstractUser):
    USER_ROLE = 'user'
  
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    role = models.CharField(max_length=255, default=USER_ROLE)
    join_date = models.DateField(default=timezone.now)
    join_time = models.TimeField(default=timezone.now)
    installer=models.ForeignKey(Installer,on_delete=models.CASCADE,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class House(models.Model):
    name=models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses')  # This is the ForeignKey field

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    house=models.ForeignKey(House,on_delete=models.CASCADE)




class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=17, unique=True,null=True,blank=True)




 
    

class DeviceConfiguration(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    device_password = models.CharField(max_length=255)
    
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



class MacIpMapping(models.Model):
    mac_address = models.CharField(max_length=17, unique=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.mac_address} - {self.ip_address}"
    

class DeviceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    ip_address = models.GenericIPAddressField()
    current = models.FloatField()
    power = models.CharField(max_length=50)
    voltage = models.FloatField()
    status=models.CharField(max_length=50)
    time = models.DateTimeField(null=True, blank=True, auto_now_add=True)


    def __str__(self):
        return self.ip_address
    

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    network_ssid = models.CharField(max_length=100, blank=True)
    network_password = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.network_ssid
    

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    device_ip = models.GenericIPAddressField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=3)
    processed = models.BooleanField(default=False)    
    




    


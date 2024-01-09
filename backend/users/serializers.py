from rest_framework import serializers
from .models import User,House,Room,Device,DeviceConfiguration,MacIpMapping,DeviceData,UserProfile,Schedule,Installer





class DateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value.strftime('%Y-%m-%d')

class TimeField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return value.strftime('%H:%M:%S')
    


class UserSerializer(serializers.ModelSerializer):

    join_date = DateField()
    join_time = TimeField()

    class Meta:
        model=User
        fields = ['id', 'name', 'email','password', 'role', 'join_date', 'join_time']
        extra_kwargs={
            'password':{'write_only':True}
        }


    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance 


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class DeviceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConfiguration
        fields = '__all__'


class MacIpMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MacIpMapping
        fields = '__all__'

class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields ='__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user','image', 'network_ssid', 'network_password']

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        user_profile = UserProfile.objects.create(**validated_data)
        if image:
            user_profile.image = image
            user_profile.save()
        return user_profile
    

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class InstallerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installer
        fields = ['name', 'email', 'password','devices']


class InstallerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installer
        fields = ['email', 'password']        















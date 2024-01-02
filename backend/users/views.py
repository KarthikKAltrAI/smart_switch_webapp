from http.client import NOT_FOUND
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,HouseSerializer,DeviceSerializer,RoomSerializer,DeviceConfigurationSerializer,DeviceDataSerializer,UserProfileSerializer
from .models import User,Room,House,Device,DeviceConfiguration,DeviceData,UserProfile
from rest_framework import viewsets
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import status
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from time import sleep
import socket
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.utils.dateparse import parse_datetime
from django.db.models import Sum















# Register
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Login
"""class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {'jwt': token}  # Set the data attribute correctly
        return response"""
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Use Django's built-in authentication system
        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed('Incorrect email or password!')

        # You can return a simple success message or user data
        return Response({
            'message': 'Login successful',
            'user_id': user.id,
            'email': user.email,
            'name':user.name
            # You can add more user details here if needed
        })
    

"""class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        serializer = UserSerializer(user)
        return Response(serializer.data)"""
User = get_user_model()

class UserView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({'user_id': user.id})
        else:
            raise AuthenticationFailed('Unauthenticated')

         

# LogoutView
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response
  
        
class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


    
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})
    
    @action(detail=False, methods=['get'])
    def user_houses(self, request, id):
        user_houses = self.get_queryset().filter(user=id)
        serializer = self.get_serializer(user_houses, many=True)
        return Response(serializer.data)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})
    

class DeviceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = DeviceConfiguration.objects.all()
    serializer_class = DeviceConfigurationSerializer


    def create(self, request, *args, **kwargs):
        # Check if data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    def list(self, request, *args, **kwargs):
        # Get all DeviceConfigurations
        queryset = DeviceConfiguration.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # Get DeviceConfiguration by ID
        queryset = DeviceConfiguration.objects.filter(pk=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

  



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(detail=True, methods=['get'])
    def user_details(self, request, pk=None):
        user = self.get_object()

        user_data = UserSerializer(user).data

        # Get all houses, rooms, devices, and device configurations related to the user
        houses = HouseSerializer(user.houses.all(), many=True).data  # Use the correct related name here
        rooms = RoomSerializer(Room.objects.filter(user=user), many=True).data
        devices = DeviceSerializer(Device.objects.filter(user=user), many=True).data
        device_configs = DeviceConfigurationSerializer(DeviceConfiguration.objects.filter(user=user), many=True).data

        response_data = {
            'user': user_data,
            'houses': houses,
            'rooms': rooms,
            'devices': devices,
            'device_configurations': device_configs,
        }

        return Response(response_data)
    




class UserDetailsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def user_details(self, request):
        user = request.user  # Access the authenticated user directly

        user_data = UserSerializer(user).data

        # Get all houses, rooms, devices, and device configurations related to the user
        houses = House.objects.filter(user=user)
        rooms = Room.objects.filter(user=user)
        devices = Device.objects.filter(user=user)
        device_configs = DeviceConfiguration.objects.filter(user=user)

        # Count the number of each type
        house_count = houses.count()
        room_count = rooms.count()
        device_count = devices.count()
        device_config_count = device_configs.count()

        response_data = {
            'user': user_data,
            'houses': house_count,
            'rooms': room_count,
            'devices': device_count,
            'device_configurations': device_config_count,
        }

        return Response(response_data)
    
class UserDetailsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def user_details(self, request):
        user = request.user  # Access the authenticated user directly

        user_data = UserSerializer(user).data

        # Get all houses, rooms, devices, and device configurations related to the user
        houses = House.objects.filter(user=user)
        rooms = Room.objects.filter(user=user)
        devices = Device.objects.filter(user=user)
        device_configs = DeviceConfiguration.objects.filter(user=user)

        # Count the number of each type
        house_count = houses.count()
        room_count = rooms.count()
        device_count = devices.count()
        device_config_count = device_configs.count()

        response_data = {
            'user': user_data,
            'houses': house_count,
            'rooms': room_count,
            'devices': device_count,
            'device_configurations': device_config_count,
        }

        return Response(response_data)
    



class HouseRoomsView(APIView):

    def get(self, request, house_id):
        try:
            rooms = Room.objects.filter(house_id=house_id)
            serializer = RoomSerializer(rooms, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        

#getting devices of particular rooms
class RoomDevicesView(APIView):

    def get(self, request, room_id):
        try:
            devices = Device.objects.filter(room_id=room_id)
            serializer = DeviceSerializer(devices, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        


#ip
class DeviceDataView(APIView):
    def post(self, request):
        data = []
        for ip, values in request.data.items():
            data.append({
                'ip_address': ip,
                'current': values.get('CURRENT'),
                'power': values.get('POWER'),
                'voltage': values.get('VOLTAGE'),
                'user': values.get('user'),
                'status':values.get('status')
               
            })

        serializer = DeviceDataSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
    def get(self, request, user_id):
        try:
            # Fetching DeviceData objects related to a specific user
            user = get_object_or_404(User, pk=user_id)
            device_data = DeviceData.objects.filter(user=user)
            # Serialize the queryset using many=True since it might return multiple objects
            serializer = DeviceDataSerializer(device_data, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except DeviceData.DoesNotExist:
            return Response({'error': 'Device Data Not Found'}, status=status.HTTP_404_NOT_FOUND)    
    


#getting device-congig of user
class UserDeviceDataView(APIView):
    def get(self, request, user_id):
        device_data = DeviceData.objects.filter(user=user_id)
        serializer = DeviceDataSerializer(device_data, many=True)
        return Response(serializer.data)



#getting devices of particular user
class UserDevicesView(APIView):
    def get(self, request, user_id):
        devices = Device.objects.filter(user_id=user_id)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)                              
    


#getting based on latest ip
class IpviewSet(APIView):
    def get(self, request, ip_address):
        try:
            device_data = DeviceData.objects.filter(ip_address=ip_address).latest('id')
            serializer = DeviceDataSerializer(device_data)
            return Response({ip_address: serializer.data})
        except DeviceData.DoesNotExist:
            return Response({'error': 'Device with given IP not found'}, status=status.HTTP_404_NOT_FOUND)

class HistoryIP(APIView):
    def get(self, request, ip_address):
            device_data = DeviceData.objects.filter(ip_address=ip_address)
            serializer = DeviceDataSerializer(device_data, many=True)
            return Response(serializer.data)

#getting based on day
class MonthView(viewsets.ModelViewSet):
    serializer_class = DeviceDataSerializer

    def get_by_month(self, request, *args, **kwargs):
        # Get DeviceConfigurations by month
        month = request.query_params.get('month', timezone.now().month)
        queryset = DeviceData.objects.filter(time__month=month)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)     
             
       
        
#getting_details_based_on_date
class DeviceConfigurationByDateView(viewsets.ModelViewSet):
    serializer_class = DeviceDataSerializer

    def get_by_date(self, request,*args,**kwargs):
        date=request.query_params.get('date',timezone.now().date)
        queryset=DeviceData.objects.filter(time=date)
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)
        """try:
            # Assuming date is in the format YYYY-MM-DD
            start_date = datetime.strptime(date, "%Y-%m-%d")
            end_date = start_date + datetime.timedelta(days=1)

            device_data = DeviceData.objects.filter(time__range=(start_date, end_date))
            serializer = DeviceDataSerializer(device_data, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)"""
        



#GETTING_TOTAL_POWER_OF_PARTICULAR_IP
class TotalPowerView(APIView):
    def get(self, request, ip_address):
        total_power = DeviceData.objects.filter(ip_address=ip_address).aggregate(Sum('power'))
        if total_power['power__sum'] is not None:
            return Response({'ip_address': ip_address, 'total_power': total_power['power__sum']})
        else:
            return Response({'error': 'No data found for the given IP address'}, status=status.HTTP_404_NOT_FOUND)



#GETTING_POWER_CONSUMPTION_BASED_ON_PEROID
def get_start_of_period(period):
    now = timezone.now()
    if period == 'daily':
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'weekly':
        return now - timezone.timedelta(days=now.weekday())
    elif period == 'monthly':
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == 'yearly':
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)        
        



#MAIN-LOGIC

class PowerConsumptionView(APIView):
     def get(self, request, ip_address, period):
        start_of_period = get_start_of_period(period)
        total_power = DeviceData.objects.filter(
            ip_address=ip_address, 
            time__gte=start_of_period
        ).aggregate(Sum('power'))['power__sum'] or 0

        return Response({
            'ip_address': ip_address,
            period + '_total': total_power,
        })
#getting as list

     
class VoltageListView(APIView):
   def get(self, request, ip_address):
        # Fetch start and end dates from the query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Parse dates
        start_datetime = parse_datetime(start_date) if start_date else None
        end_datetime = parse_datetime(end_date) if end_date else None

        # Base query
        queryset = DeviceData.objects.filter(ip_address=ip_address)

        # Filter by date range if both dates are provided
        if start_datetime and end_datetime:
            queryset = queryset.filter(time__range=[start_datetime, end_datetime])
        # Optionally handle cases where only one of the dates is provided

        # Extract the data
        data = queryset.order_by('time').values('time', 'voltage', 'current', 'power')

        # Convert to list of dictionaries
        data_list = list(data)

        return Response(data_list)
        """def get(self, request, ip_address):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Parse dates
        start_datetime = parse_datetime(start_date) if start_date else None
        end_datetime = parse_datetime(end_date) if end_date else None

        # Base query
        queryset = DeviceData.objects.filter(ip_address=ip_address)

        # Filter by date range if both dates are provided
        if start_datetime and end_datetime:
            queryset = queryset.filter(time__range=[start_datetime, end_datetime])

        # Calculate sums
        total_voltage = queryset.aggregate(Sum('voltage')).get('voltage__sum') or 0
        total_current = queryset.aggregate(Sum('current')).get('current__sum') or 0
        total_power = queryset.aggregate(Sum('power')).get('power__sum') or 0

        return Response({
            'total_voltage': total_voltage,
            'total_current': total_current,
            'total_power': total_power
        })"""

class CurrentListView(APIView):
    def get(self, request, ip_address):
        # Filter all records by IP address and only get the 'current' field
        currents = DeviceData.objects.filter(ip_address=ip_address).values_list('current', flat=True)
        return Response({'currents': list(currents)})
    

class PowerListView(APIView):
    def get(self, request, ip_address):
        # Filter all records by IP address and only get the 'power' field
        powers = DeviceData.objects.filter(ip_address=ip_address).values_list('power', flat=True)
        return Response({'powers': list(powers)})    
    
    
class PowerMonthlyListView(APIView):
    def get(self, request, ip_address, year, month):
        # Filter records by IP address and month
        start_date = timezone.datetime(year=int(year), month=int(month), day=1)
        if month == '12':
            end_date = timezone.datetime(year=int(year)+1, month=1, day=1)
        else:
            end_date = timezone.datetime(year=int(year), month=int(month)+1, day=1)
        
        powers = DeviceData.objects.filter(
            ip_address=ip_address,
            time__range=[start_date, end_date]
        ).values_list('power', flat=True)

        return Response({'powers': list(powers)})
    
        
    

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save()
class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__id'  
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs.get('pk')}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user__id'
    lookup_url_kwarg = 'user_id'

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        try:
            return UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise NOT_FOUND("UserProfile with this user ID does not exist.")   
        


class ClearUserProfileFieldsView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def partial_update(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user_profile = get_object_or_404(UserProfile, user__id=user_id)

        # Clear the specific fields
        user_profile.image.delete(save=False)  # Delete the image file
        user_profile.network_ssid = ""
        user_profile.network_password = ""
        user_profile.save()

        return Response(status=status.HTTP_204_NO_CONTENT)           
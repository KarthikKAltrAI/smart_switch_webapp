from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,HouseSerializer,DeviceSerializer,RoomSerializer,DeviceConfigurationSerializer,DeviceDataSerializer
from .models import User,Room,House,Device,DeviceConfiguration,DeviceData
from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models.functions import TruncMonth
from rest_framework import status
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from time import sleep
import socket
from rest_framework.decorators import api_view
from django.http import JsonResponse
from scapy.all import ARP, Ether, srp
from django.shortcuts import get_object_or_404
from datetime import datetime








import jwt
import datetime

# Register
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Login
class LoginView(APIView):
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
        return response
class UserView(APIView):
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
        return Response(serializer.data)

         

# LogoutView
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response
    
class UserFieldMixin:
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
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
        
# getting ip
class Ipadd(APIView):
    @api_view(['GET'])
    def get_ip_by_mac(request, mac_address):
        try:
            ip = socket.gethostbyname(socket.gethostname())  # local ip
        except:
            ip = '127.0.0.1'

        nm = NmapProcess(f'{ip}/24', options="-sP")
        nm.run_background()

        while nm.is_running():
            sleep(2)

        nmap_report = NmapParser.parse(nm.stdout)
        
        print("Nmap Output:", nm.stdout)  # Debugging statement

        res = next(
            filter(lambda n: n.mac == mac_address.strip().upper(),
                   filter(lambda host: host.is_up(), nmap_report.hosts)),
            None
        )

        if res is None:
            return Response({"error": "Host is down or Mac address does not exist"}, status=404)
        else:
            return Response({"mac_address": mac_address, "ip_address": res.address})



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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,HouseSerializer,DeviceSerializer,RoomSerializer,DeviceConfigurationSerializer
from .models import User,Room,House,Device,DeviceConfiguration
from rest_framework import viewsets,permissions
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models.functions import TruncMonth



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
    permission_classes = [permissions.IsAuthenticated]


    
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=['get'])
    def count(self, request):
        count = self.get_queryset().count()
        return Response({'count': count})
    

class DeviceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = DeviceConfiguration.objects.all()
    serializer_class = DeviceConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]


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

    def get_by_month(self, request, *args, **kwargs):
        # Get DeviceConfigurations by month
        month = request.query_params.get('month', timezone.now().month)
        queryset = DeviceConfiguration.objects.filter(time__month=month)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
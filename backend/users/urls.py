from django.urls import path,include
from .views import RegisterView,LoginView,UserView,LogoutView,HouseViewSet,RoomViewSet,DeviceViewSet,DeviceConfigurationViewSet
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserView.as_view()),
    path('logout',LogoutView.as_view()),
    
    path('houses/', HouseViewSet.as_view({'get': 'list', 'post': 'create'}), name='house-list'),
    path('houses/<int:pk>/', HouseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='house-detail'),

    path('rooms/', RoomViewSet.as_view({'get': 'list', 'post': 'create'}), name='room-list'),
    path('rooms/<int:pk>/', RoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='room-detail'),

    path('devices/', DeviceViewSet.as_view({'get': 'list', 'post': 'create'}), name='device-list'),
    path('devices/<int:pk>/', DeviceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='device-detail'),
    
    #COUNT
    path('houses/count/', HouseViewSet.as_view({'get': 'count'}), name='house-count'),
    path('rooms/count/', RoomViewSet.as_view({'get': 'count'}), name='room-count'),
    path('devices/count/', DeviceViewSet.as_view({'get': 'count'}), name='device-count'),

    #Device-Config

    path('device-configurations/', DeviceConfigurationViewSet.as_view({'get': 'list', 'post': 'create'}), name='device-list'),
    path('device-configuartions/<int:pk>/', DeviceConfigurationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='device-detail'),




    
]
from django.urls import path,include
from .views import DeviceConfigurationByDateView, RegisterView,LoginView,UserView,LogoutView,HouseViewSet,RoomViewSet,DeviceViewSet,DeviceConfigurationViewSet,UserViewSet,UserDetailsViewSet,HouseRoomsView,RoomDevicesView,Ipadd,DeviceDataView,UserDeviceDataView,UserDevicesView,IpviewSet,MonthView,HistoryIP
from rest_framework.routers import DefaultRouter
from .consumers import DeviceDataConsumer


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
    path('device-configurations/<int:pk>/', DeviceConfigurationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='device-detail'),
    path('device-configurations/get_by_month/', MonthView.as_view({'get': 'get_by_month'}), name='device-configurations-by-month'),


    #getting,counting_users
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/total_users/', UserViewSet.as_view({'get': 'total_users'}), name='total-users'),
    path('users/<int:pk>/details/', UserViewSet.as_view({'get': 'user_details'}), name='user-details'),

    #counting homes of particular user
    path('users/user-details/<int:pk>/', UserDetailsViewSet.as_view({'get': 'user_details'}), name='user-details'),


     #getting house of particular user
     path('houses/user_houses/<int:id>', HouseViewSet.as_view({'get': 'user_houses'}), name='user-houses'),

    #ipaddress
    path('get_ip/<str:mac_address>/', Ipadd.get_ip_by_mac, name='get_ip_by_mac'),



    #getting rooms of particular house
    path('houses/<int:house_id>/rooms/', HouseRoomsView.as_view(), name='house-rooms'),

    #getting devices of particular room
     path('rooms/<int:room_id>/devices/', RoomDevicesView.as_view(), name='room-devices'),


     #posting as list with-ip
    path('device-data/', DeviceDataView.as_view(), name='device-data-list'),
    path('device-data/ip/latest/<str:ip_address>/', IpviewSet.as_view(), name='device-data-detail'),

    #getting details of device of particular user
    path('device-data/<int:user_id>/', UserDeviceDataView.as_view(), name='user-device-data'),

    #getting device name of particular user
    path('users/devices/<int:user_id>', UserDevicesView.as_view(), name='user-devices'),

    #GETTING_DEVICEDATA_BY_DATE
    path('device-data/date/', DeviceConfigurationByDateView.as_view({'get': 'get_by_date'}), name='device-configurations-by-date'),

    #history of Ip
    path('device-data/<str:ip_address>/', HistoryIP.as_view(), name='device-data-detail'),


    
    






 

]
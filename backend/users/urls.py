from django.urls import path
from .views import  CreateScheduleView, DeviceConfigurationByDateView, PowerDataView, RegisterView,LoginView, ScheduleDetailView, Scheduleget, UserPowerDataView,UserView,LogoutView,HouseViewSet,RoomViewSet,DeviceViewSet,DeviceConfigurationViewSet,UserViewSet,UserDetailsViewSet,HouseRoomsView,RoomDevicesView,DeviceDataView,UserDeviceDataView,UserDevicesView,IpviewSet,MonthView,HistoryIP,TotalPowerView,PowerConsumptionView,VoltageListView,CurrentListView,PowerListView,PowerMonthlyListView,UserProfileListCreateView,UserProfileDetailView,UserProfileUpdateView,ClearUserProfileFieldsView



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

    


    #getting rooms of particular house
    path('houses/<int:house_id>/rooms/', HouseRoomsView.as_view(), name='house-rooms'),

    #getting devices of particular room
    path('rooms/<int:room_id>/devices/', RoomDevicesView.as_view(), name='room-devices'),

    #posting as list with-ip
    path('device-data/', DeviceDataView.as_view(), name='device-data-list'),

    #getting_latest_ip
    path('device-data/ip/latest/<str:ip_address>/', IpviewSet.as_view(), name='device-data-detail'),

    #getting details of device of particular user
    path('device-data/<int:user_id>/', UserDeviceDataView.as_view(), name='user-device-data'),

    #getting device name_of_particular_user
    path('users/devices/<int:user_id>', UserDevicesView.as_view(), name='user-devices'),

    #GETTING_DEVICEDATA_BY_DATE
    path('device-data/date/', DeviceConfigurationByDateView.as_view({'get': 'get_by_date'}), name='device-configurations-by-date'),

    #history of Ip
    path('device-data/<str:ip_address>/', HistoryIP.as_view(), name='device-data-detail'),

    #TOTAL_POWER_OF_PARTICULAR_IP[DEV]
    path('device-data/total-power/<str:ip_address>/', TotalPowerView.as_view(), name='total-power'),

    #power-consumption
    path('device-data/<str:ip_address>/<str:period>/', PowerConsumptionView.as_view(), name='power-consumption'),

    #current-list
    path('device-current-list/<str:ip_address>/', CurrentListView.as_view(), name='device-current-list'),




    #power-list
    path('device-power-list/<str:ip_address>/', PowerListView.as_view(), name='device-power-list'),


    
    path('device-voltage-list/<str:ip_address>/', VoltageListView.as_view(), name='device-voltage-list'),

    path('device-power-monthly-list/<str:ip_address>/<int:year>/<int:month>/', PowerMonthlyListView.as_view(), name='device-power-monthly-list'),


    path('profiles/', UserProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('user-profile/<int:user_id>/', UserProfileUpdateView.as_view(), name='update-user-profile'),
    path('user-profile/clear-fields/<int:pk>/', ClearUserProfileFieldsView.as_view(), name='clear-user-profile-fields'),
    path('create_schedule/', CreateScheduleView.as_view(), name='create_schedule'),
    path('getschedule/<int:user_id>',Scheduleget.as_view(),name='schedule-get'),
    path('schedule/<int:schedule_id>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('power_data/<str:time_range>/', PowerDataView.as_view(), name='power_data'),
    path('userpower_data/<str:time_range>/<int:user_id>/<str:ip_address>/', UserPowerDataView.as_view(), name='user_power_data'),















 

]
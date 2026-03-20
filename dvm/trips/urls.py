from django.urls import path
from .views import request_ride_ssr,create_trip_ssr,available_trips_ssr,driver_dashboard_view,available_requests_view,join_trip_request

urlpatterns = [
    path('request-ride/', request_ride_ssr, name='request-ride-ssr'),
    path('create-trip/', create_trip_ssr, name='create-trip-ssr'),
    path('available-trips/', available_trips_ssr, name='available-trips-ssr'),
    path('dashboard/', driver_dashboard_view, name='driver-dashboard'),
    path('available-requests/', available_requests_view, name='available-requests'),
    path('join-trip/<int:trip_id>/', join_trip_request, name='accept-ride'),
]
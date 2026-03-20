from django.shortcuts import render, redirect
from .models import CarPoolRequest
from network.models import Node
from .utils import get_shortest_path
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def request_ride_ssr(request):
    if request.user.role != 'passenger':
        return redirect('create-trip-ssr')

    nodes = Node.objects.all()

    if request.method == 'POST':
        pickup_id = request.POST.get('pickup_node')
        dropoff_id = request.POST.get('dropoff_node')
        
        pickup_node = Node.objects.get(id=pickup_id)
        dropoff_node = Node.objects.get(id=dropoff_id)

        path = get_shortest_path(pickup_node, dropoff_node)
        if not path:
            messages.error(request, "No route found between these points!")
            return redirect('request-ride-ssr')

        fare = Decimal(10 + ((len(path) - 1) * 50))

        CarPoolRequest.objects.create(
            passenger=request.user,
            pickup_node=pickup_node,
            dropoff_node=dropoff_node,
            estimated_fare=fare,
            status='pending'
        )
        messages.success(request, f"Ride requested! Estimated fare: ₹{fare}")
        return redirect('available-trips-ssr') # Send them to see who's driving

    return render(request, 'trips/request_ride.html', {'nodes': nodes})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip
from network.models import Node
from .utils import get_shortest_path

@login_required
def create_trip_ssr(request):
    if request.user.role != 'driver':
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    nodes = Node.objects.all()

    if request.method == 'POST':
        start_node_id = request.POST.get('start_node')
        end_node_id = request.POST.get('end_node')
        max_seats = request.POST.get('max_passengers')

        start_node = Node.objects.get(id=start_node_id)
        end_node = Node.objects.get(id=end_node_id)

        path = get_shortest_path(start_node, end_node)
        
        if not path:
            messages.error(request, "No valid route found for this trip!")
            return redirect('create-trip-ssr')

        Trip.objects.create(
            driver=request.user,
            start_node=start_node,
            end_node=end_node,
            current_node=start_node,
            max_passengers=max_seats,
            planned_route=path,
            status='planned'
        )

        messages.success(request, f"Trip created successfully! Route: {' -> '.join(map(str, path))}")
        return redirect('available-trips-ssr')

    return render(request, 'trips/create_trip.html', {'nodes': nodes})

from django.shortcuts import render, redirect
from .models import Trip
from django.contrib.auth.decorators import login_required

@login_required
def available_trips_ssr(request):
    if request.user.role == 'driver':
        return redirect('driver-dashboard') 

    trips = Trip.objects.filter(status__in=['planned', 'active'], max_passengers__gt=0)

    return render(request, 'trips/available_trips.html', {'trips': trips})

from django.db.models import Sum

@login_required
def driver_dashboard_view(request):
    if request.user.role != 'driver':
        return redirect('request-ride-ssr')

    current_trip = Trip.objects.filter(driver=request.user, status__in=['planned', 'active']).first()

    past_trips = Trip.objects.filter(driver=request.user, status='completed').order_by('-created_at')

    total_earnings = CarPoolRequest.objects.filter(
        trip__driver=request.user, 
        status='accepted'
    ).aggregate(Sum('estimated_fare'))['estimated_fare__sum'] or 0

    return render(request, 'trips/driver_dashboard.html', {
        'current_trip': current_trip,
        'past_trips': past_trips,
        'total_earnings': total_earnings
    })

@login_required
def available_requests_view(request):
    if request.user.role != 'driver':
        return redirect('request-ride-ssr')

    pending_requests = CarPoolRequest.objects.filter(status='pending')

    return render(request, 'trips/available_requests.html', {
        'requests': pending_requests
    })

@login_required
def join_trip_request(request, trip_id):
    if request.method == 'POST':
        trip = Trip.objects.get(id=trip_id)
        
        CarPoolRequest.objects.create(
            passenger=request.user,
            trip=trip,
            pickup_node=trip.start_node,
            dropoff_node=trip.end_node,
            status='pending',
            estimated_fare=100 
        )
        
        messages.success(request, f"Request sent to {trip.driver.username}! Wait for them to accept.")
        return redirect('available-trips-ssr')
    
    return redirect('available-trips-ssr')
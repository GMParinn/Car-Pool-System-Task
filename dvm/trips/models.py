from django.db import models
from django.conf import settings

class Trip(models.Model):

    Trip_status = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
        ('cancelled', 'Cancelled')
    )

    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='trips_driven')

    start_node = models.ForeignKey('network.Node', on_delete=models.RESTRICT, related_name='trips_starting_here')
    end_node = models.ForeignKey('network.Node', on_delete=models.RESTRICT, related_name='trips_ending_here')
    current_node = models.ForeignKey('network.Node', on_delete=models.RESTRICT, related_name='current_trips_here')

    max_passengers = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, choices=Trip_status, default='planned')

    planned_route= models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Trip {self.id}: {self.driver.username} {self.status}"
    
class CarPoolRequest(models.Model):

    Request_status=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    )

    passenger = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='ride_requests')
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='requests', null=True, blank=True)

    pickup_node = models.ForeignKey('network.Node', on_delete=models.RESTRICT, related_name='pickups')
    dropoff_node = models.ForeignKey('network.Node', on_delete=models.RESTRICT, related_name='dropoffs')

    status = models.CharField(max_length=20, choices=Request_status, default='pending')

    estimated_fare = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        trip_id = self.trip.id if self.trip else "Pending"
        return f"Request {self.id}: {self.passenger.username} -> Trip {trip_id}"
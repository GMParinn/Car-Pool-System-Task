from rest_framework import serializers
from .models import CarPoolRequest, Trip

class CarPoolRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarPoolRequest
        # Adjust 'number_of_passengers' if you named it differently in your models.py!
        fields = ['id', 'pickup_node', 'dropoff_node', 'status','created_at',]
        read_only_fields = ['status', 'passenger']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'start_node', 'end_node','max_passangers', 'status']
        # The driver shouldn't be able to fake their status or ID
        read_only_fields = ['status', 'driver']
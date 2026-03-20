from django.contrib import admin
from .models import Trip, CarPoolRequest

class TripAdmin(admin.ModelAdmin):

    list_display=('id', 'driver', 'status', 'start_node', 'end_node', 'current_node',)

    list_filter=('status',)

    search_fields=('driver__username',)

class CarPoolRequestAdmin(admin.ModelAdmin):
    list_display=('id', 'passenger', 'status', 'trip', 'estimated_fare',)

    list_filter=('status',)

    search_fields=('passenger__username',)

admin.site.register(Trip, TripAdmin)
admin.site.register(CarPoolRequest, CarPoolRequestAdmin)

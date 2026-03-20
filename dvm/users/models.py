from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = (
        ('passenger','Passenger'),
        ('driver','Driver'),
        ('admin','Admin'),
    )

    role = models.CharField(max_length=20, choices = ROLE_CHOICES, default='passenger')

    wallet_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

class Transaction(models.Model):

    TRANSACTION_TYPES= (
        ('top_up', 'Wallet Top Up'),
        ('driver_earning', 'Driver Earnings'),
        ('fare_payment', 'Fare Payment')
    )

    transaction_types = models.CharField(max_length=20, choices = TRANSACTION_TYPES)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    timestamp = models.DateTimeField(auto_now_add=True)

    trip = models.ForeignKey('trips.Trip', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_by.username}|{self.transaction_types}|{self.amount}|{self.timestamp}|{self.trip}"
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('cleaning', 'Cleaning'),
        ('maintenance', 'Maintenance'),
    ]
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"

class Staff(models.Model):
    DEPARTMENT_CHOICES = [
        ('kitchen', 'Kitchen'),
        ('housekeeping', 'Housekeeping'),
        ('maintenance', 'Maintenance'),
        ('spa', 'Spa'),
        ('cab', 'Cab'),
        ('reception', 'Reception'),
        ('manager', 'Manager'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    whatsapp_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    department = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Room {self.room.room_number} - {self.department} - {self.status}"

class FoodOrder(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    items = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room.room_number} - Food Order"

class CabBooking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    people = models.IntegerField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room.room_number} - Cab to {self.destination}"

class SpaBooking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    people = models.IntegerField()
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room.room_number} - Spa {self.service_type}"


class Guest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin_date = models.DateTimeField(auto_now_add=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - Room {self.room.room_number}"
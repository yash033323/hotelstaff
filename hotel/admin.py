from django.contrib import admin
from .models import Room, Staff, Task, FoodOrder, CabBooking, SpaBooking, Guest

admin.site.register(Room)
admin.site.register(Staff)
admin.site.register(Task)
admin.site.register(FoodOrder)
admin.site.register(CabBooking)
admin.site.register(SpaBooking)
admin.site.register(Guest)
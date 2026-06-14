from django.urls import path
from . import views

urlpatterns = [
    path('staff/login/', views.staff_login, name='login'),
    path('staff/logout/', views.staff_logout, name='logout'),
    path('staff/kitchen/', views.kitchen, name='kitchen'),
    path('staff/kitchen/complete/<int:order_id>/', views.kitchen_complete, name='kitchen_complete'),
    path('staff/housekeeping/', views.housekeeping, name='housekeeping'),
    path('staff/housekeeping/complete/<int:task_id>/', views.housekeeping_complete, name='housekeeping_complete'),
    path('staff/maintenance/', views.maintenance, name='maintenance'),
    path('staff/maintenance/complete/<int:task_id>/', views.maintenance_complete, name='maintenance_complete'),
    path('staff/spa/', views.spa, name='spa'),
    path('staff/spa/complete/<int:booking_id>/', views.spa_complete, name='spa_complete'),
    path('staff/cab/', views.cab, name='cab'),
    path('staff/cab/complete/<int:booking_id>/', views.cab_complete, name='cab_complete'),
    path('staff/reception/', views.reception, name='reception'),
    path('staff/reception/checkin/<int:room_id>/', views.checkin, name='checkin'),
    path('staff/reception/checkout/<int:room_id>/', views.checkout, name='checkout'),
    path('staff/manager/', views.manager, name='manager'),
    path('room/', views.room_service, name='room_service'),
    path('room/food/', views.food_order, name='food_order'),
    path('room/housekeeping/', views.housekeeping_request, name='housekeeping_request'),
    path('room/maintenance/', views.maintenance_request, name='maintenance_request'),
    path('room/spa/', views.spa_request, name='spa_request'),
    path('room/cab/', views.cab_request, name='cab_request'),
    path('qr/', views.generate_qr, name='generate_qr'),
    ]
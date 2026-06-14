from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Room, Staff, Task, FoodOrder, CabBooking, SpaBooking, Guest
from twilio.rest import Client
from django.conf import settings
import qrcode
import io
from django.http import HttpResponse

def send_whatsapp(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=f'whatsapp:{to_number}',
        body=message
    )

def staff_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            dept = user.staff.department
            if dept == 'kitchen':
                return redirect('/staff/kitchen/')
            elif dept == 'housekeeping':
                return redirect('/staff/housekeeping/')
            elif dept == 'maintenance':
                return redirect('/staff/maintenance/')
            elif dept == 'spa':
                return redirect('/staff/spa/')
            elif dept == 'cab':
                return redirect('/staff/cab/')
            elif dept == 'reception':
                return redirect('/staff/reception/')
            elif dept == 'manager':
                return redirect('/staff/manager/')
        else:
            error = 'Wrong username or password!'
    return render(request, 'hotel/login.html', {'error': error})

def staff_logout(request):
    logout(request)
    return redirect('/staff/login/')

@login_required(login_url='/staff/login/')
def kitchen(request):
    tasks = FoodOrder.objects.filter(status='pending')
    completed = FoodOrder.objects.filter(status='completed')
    return render(request, 'hotel/kitchen.html', {'tasks': tasks, 'completed': completed})

def kitchen_complete(request, order_id):
    order = FoodOrder.objects.get(id=order_id)
    order.status = 'completed'
    order.save()
    return redirect('/staff/kitchen/')

@login_required(login_url='/staff/login/')
def housekeeping(request):
    tasks = Task.objects.filter(department='housekeeping', status='pending')
    completed = Task.objects.filter(department='housekeeping', status='completed')
    return render(request, 'hotel/housekeeping.html', {'tasks': tasks, 'completed': completed})

def housekeeping_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'completed'
    task.assigned_to = request.user.staff
    task.completed_at = timezone.now()
    task.save()
    task.room.status = 'available'
    task.room.save()
    return redirect('/staff/housekeeping/')

@login_required(login_url='/staff/login/')
def maintenance(request):
    tasks = Task.objects.filter(department='maintenance', status='pending')
    completed = Task.objects.filter(department='maintenance', status='completed')
    return render(request, 'hotel/maintenance.html', {'tasks': tasks, 'completed': completed})

def maintenance_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'completed'
    task.assigned_to = request.user.staff
    task.completed_at = timezone.now()
    task.save()
    return redirect('/staff/maintenance/')

@login_required(login_url='/staff/login/')
def spa(request):
    tasks = SpaBooking.objects.filter(status='pending')
    completed = SpaBooking.objects.filter(status='completed')
    return render(request, 'hotel/spa.html', {'tasks': tasks, 'completed': completed})

def spa_complete(request, booking_id):
    booking = SpaBooking.objects.get(id=booking_id)
    booking.status = 'completed'
    booking.save()
    return redirect('/staff/spa/')

@login_required(login_url='/staff/login/')
def cab(request):
    tasks = CabBooking.objects.filter(status='pending')
    completed = CabBooking.objects.filter(status='completed')
    return render(request, 'hotel/cab.html', {'tasks': tasks, 'completed': completed})

def cab_complete(request, booking_id):
    booking = CabBooking.objects.get(id=booking_id)
    booking.status = 'completed'
    booking.save()
    return redirect('/staff/cab/')

@login_required(login_url='/staff/login/')
def reception(request):
    rooms = Room.objects.all()
    available_rooms = rooms.filter(status='available').count()
    occupied_rooms = rooms.filter(status='occupied').count()
    cleaning_rooms = rooms.filter(status='cleaning').count()
    guests = Guest.objects.filter(is_checked_out=False)
    guest_history = Guest.objects.filter(is_checked_out=True)
    return render(request, 'hotel/reception.html', {
        'rooms': rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'cleaning_rooms': cleaning_rooms,
        'guests': guests,
        'guest_history': guest_history,
    })

def checkin(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        Guest.objects.create(
            name=name,
            phone=phone,
            room=room,
        )
        room.status = 'occupied'
        room.save()
        return redirect('/staff/reception/')
    return render(request, 'hotel/checkin.html', {'room': room})

def checkout(request, room_id):
    room = Room.objects.get(id=room_id)
    guest = Guest.objects.filter(room=room, is_checked_out=False).first()
    if guest:
        guest.checkout_date = timezone.now()
        guest.total_bill = room.price
        guest.is_checked_out = True
        guest.save()
    room.status = 'cleaning'
    room.save()
    Task.objects.create(
        room=room,
        department='housekeeping',
        description=f'Clean room after checkout - Room {room.room_number}',
        status='pending'
    )
    return redirect('/staff/reception/')

@login_required(login_url='/staff/login/')
def manager(request):
    staff = Staff.objects.all()
    rooms = Room.objects.all()
    tasks = Task.objects.all()
    pending_tasks = tasks.filter(status='pending').count()
    completed_tasks = tasks.filter(status='completed').count()
    return render(request, 'hotel/manager.html', {
        'staff': staff,
        'rooms': rooms,
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    })

def room_service(request):
    error = None
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        try:
            room = Room.objects.get(room_number=room_number)
            request.session['room_id'] = room.id
            request.session['room_number'] = room.room_number
            request.session['room_type'] = room.room_type
            return render(request, 'hotel/services.html', {'room': room})
        except Room.DoesNotExist:
            error = 'Room not found! Please check your room number.'
    return render(request, 'hotel/room_service.html', {'error': error})

def food_order(request):
    room_id = request.session.get('room_id')
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        items = request.POST.get('items')
        FoodOrder.objects.create(room=room, items=items)
        # Send WhatsApp to kitchen staff
        kitchen_staff = Staff.objects.filter(department='kitchen')
        for staff in kitchen_staff:
            send_whatsapp(
                staff.whatsapp_number,
                f'🍽️ NEW FOOD ORDER!\nRoom: {room.room_number}\nItems: {items}'
            )
        return render(request, 'hotel/success.html', {'message': 'Food order placed!', 'room': room})
    return render(request, 'hotel/food_order.html', {'room': room})

def housekeeping_request(request):
    room_id = request.session.get('room_id')
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        description = request.POST.get('description')
        Task.objects.create(room=room, department='housekeeping', description=description)
        # Send WhatsApp to housekeeping staff
        housekeeping_staff = Staff.objects.filter(department='housekeeping')
        for staff in housekeeping_staff:
            send_whatsapp(
                staff.whatsapp_number,
                f'🧹 NEW HOUSEKEEPING REQUEST!\nRoom: {room.room_number}\nRequest: {description}'
            )
        return render(request, 'hotel/success.html', {'message': 'Housekeeping request sent!', 'room': room})
    return render(request, 'hotel/housekeeping_request.html', {'room': room})

def maintenance_request(request):
    room_id = request.session.get('room_id')
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        description = request.POST.get('description')
        Task.objects.create(room=room, department='maintenance', description=description)
        # Send WhatsApp to maintenance staff
        maintenance_staff = Staff.objects.filter(department='maintenance')
        for staff in maintenance_staff:
            send_whatsapp(
                staff.whatsapp_number,
                f'🔧 NEW MAINTENANCE REQUEST!\nRoom: {room.room_number}\nIssue: {description}'
            )
        return render(request, 'hotel/success.html', {'message': 'Maintenance request sent!', 'room': room})
    return render(request, 'hotel/maintenance_request.html', {'room': room})

def spa_request(request):
    room_id = request.session.get('room_id')
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        date = request.POST.get('date')
        time = request.POST.get('time')
        people = request.POST.get('people')
        note = request.POST.get('note')
        SpaBooking.objects.create(room=room, service_type=service_type, date=date, time=time, people=people, note=note)
        # Send WhatsApp to spa staff
        spa_staff = Staff.objects.filter(department='spa')
        for staff in spa_staff:
            send_whatsapp(
                staff.whatsapp_number,
                f'💆 NEW SPA BOOKING!\nRoom: {room.room_number}\nService: {service_type}\nDate: {date}\nTime: {time}\nPeople: {people}'
            )
        return render(request, 'hotel/success.html', {'message': 'Spa booking confirmed!', 'room': room})
    return render(request, 'hotel/spa_request.html', {'room': room})

def cab_request(request):
    room_id = request.session.get('room_id')
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        pickup_location = request.POST.get('pickup_location')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        time = request.POST.get('time')
        people = request.POST.get('people')
        note = request.POST.get('note')
        CabBooking.objects.create(room=room, pickup_location=pickup_location, destination=destination, date=date, time=time, people=people, note=note)
        # Send WhatsApp to cab staff
        cab_staff = Staff.objects.filter(department='cab')
        for staff in cab_staff:
            send_whatsapp(
                staff.whatsapp_number,
                f'🚗 NEW CAB BOOKING!\nRoom: {room.room_number}\nPickup: {pickup_location}\nDestination: {destination}\nDate: {date}\nTime: {time}\nPeople: {people}'
            )
        return render(request, 'hotel/success.html', {'message': 'Cab booking confirmed!', 'room': room})
    return render(request, 'hotel/cab_request.html', {'room': room})


def generate_qr(request):
    # URL of your room service page
    url = 'http://127.0.0.1:8000/room/'

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save to buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')
HOTEL MANAGEMENT SYSTEM - PRESENTATION NOTES
====================================================

SLIDE 1 - TITLE
---------------
This project is a Hotel Management System built using Django Python framework.
It provides a complete digital solution for modern hotels including online
booking, QR code services, staff management and WhatsApp notifications.

SLIDE 2 - PROJECT OVERVIEW
---------------------------
The system has 2 websites. Website 1 is for customers to book rooms online.
Website 2 is for hotel staff to manage tasks. One QR code is placed in each
room for all in-room services. Each department has its own dashboard.
WhatsApp notifications are sent to correct staff instantly. All data is stored
in one shared database.

SLIDE 3 - SYSTEM ARCHITECTURE
-------------------------------
Website 1 handles customer bookings. Website 2 handles QR services and staff
dashboards. Both websites share the same database. When customer books on
Website 1, reception sees it on Website 2. When customer scans QR on Website 2,
correct staff gets notified instantly.

SLIDE 4 - 5 ROOM TYPES
------------------------
Hotel has 5 room types. Simple Room at 4000 rupees per night. Deluxe Room at
7000 rupees. Super Deluxe at 10000 rupees. Suite Room at 15000 rupees.
Presidential Suite at 25000 rupees. All rooms include same services like
housekeeping, food ordering, room service, WiFi, AC and TV.

SLIDE 5 - QR CODE SYSTEM
--------------------------
Each room has one unique QR code. Customer scans it with their phone. No login
is needed for customers. After scanning they can order food, request
housekeeping, report maintenance, book spa or book cab. All from one QR code.

SLIDE 6 - FOOD ORDERING
-------------------------
Customer scans QR code in room. Opens food menu on their phone. Browses food
items with prices. Selects items and adds to order. Room number is filled
automatically. Customer places order. Kitchen staff gets WhatsApp notification
instantly. Kitchen staff sees order on their dashboard and prepares food.

SLIDE 7 - STAFF DASHBOARDS
----------------------------
Each department has its own separate dashboard. Kitchen staff sees only food
orders. Housekeeping staff sees cleaning and towel requests. Maintenance staff
sees repair requests. Spa staff sees spa bookings with time slots. Cab staff
sees cab bookings with time and destination. Reception staff sees check-in,
check-out and all bookings.

SLIDE 8 - ROOM STATUS SYSTEM
------------------------------
Every room has one of 4 statuses. Green means Available and ready for booking.
Red means Occupied and guest is staying. Yellow means Cleaning after checkout.
Grey means Maintenance and under repair. When guest checks out room is
automatically set to Cleaning. Housekeeping gets WhatsApp. After cleaning is
done staff marks complete and room becomes Available again.

SLIDE 9 - MANAGER PANEL
-------------------------
Manager has full control of the system. Manager can add new staff with name,
department and WhatsApp number. Manager can remove or edit staff. Manager can
see all tasks from all departments. Manager can see all room statuses. Manager
can see all guest details and history. Manager can see bills and revenue.
Manager can see staff performance and task completion.

SLIDE 10 - WHATSAPP NOTIFICATIONS
-----------------------------------
When customer makes any request via QR code, request is saved in database.
System identifies which department should handle it. WhatsApp message is sent
to correct staff phone number. Staff opens their dashboard and sees the task.
Staff completes task and marks it done. Manager gets copy of all notifications.

SLIDE 11 - CAB & SPA BOOKING
------------------------------
For Cab booking customer enters pickup location, destination, date, time,
number of people and special note. For Spa booking customer selects service
type like massage or facial, then picks date, time, number of people and
special note. Both bookings go to correct staff dashboard with WhatsApp alert.

SLIDE 12 - TASK HISTORY & STAFF PERFORMANCE
---------------------------------------------
Every completed task is recorded with room number, task type, staff name who
completed it, and time of completion. Manager can see full history of all
tasks. Manager can also see staff performance showing how many tasks each
staff member completed today. This helps manager track efficiency.

SLIDE 13 - BOOKING ALGORITHM
------------------------------
Customer visits booking website and selects room type and dates. Fills booking
form with name, email and phone. System checks if room is available. If
available booking is saved in database. Reception gets WhatsApp notification.
On check-in day room status is set to Occupied. QR code is assigned to that
room for guest to use during their stay.

SLIDE 14 - TECHNOLOGIES USED
------------------------------
Python is the main backend language. Django is the web framework used to build
the system. SQLite is used for development database and PostgreSQL for
production. QR Code library generates unique QR codes for each room. Twilio
API sends WhatsApp notifications to staff. HTML and CSS for frontend design.
Railway cloud platform for deployment. Django Auth system for staff login.

SLIDE 15 - CONCLUSION
----------------------
This Hotel Management System is a complete digital solution. It has 2 separate
websites, 5 room types with QR code service, multi-staff dashboards for each
department, instant WhatsApp notifications, full manager control panel and will
be deployed on Railway cloud platform.

====================================================
END OF NOTES
====================================================






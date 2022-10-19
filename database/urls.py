"""
List of all the databse routes...
"""
from django.contrib import admin
from django.urls import path
from database import users
from database import subscription
from database import bus_services
from database import dining_services
from database import ccdu
from database import campus_control
from database import events

urlpatterns = [
    path("addSub/", subscription.add_sub),
    path("getSub/", subscription.get_sub),
    path("getBusSchedule/", bus_services.get_bus_schedule),
    path("followBus/", bus_services.follow_bus),
    path("getBusFollowing/", bus_services.get_bus_following),
    path("getDiningHalls/", dining_services.get_dining_halls),
    path("followDiningHall/", dining_services.follow_dh),
    path("getDiningHallFollowing/", dining_services.get_dh_following),
    path("getTime/", dining_services.getTime),
    path("bookingCCDU/", ccdu.book_session),
    path("getBookingCCDU/", ccdu.get_bookings),
    path("getCounsellors/", ccdu.get_counsellors),
    path("requestRide/", campus_control.request_ride),
    path("getAllResidences/", campus_control.get_all_residences),
    path("getAllCampuses/", campus_control.get_all_campuses),
    path("getEvents/", events.get_events),
]

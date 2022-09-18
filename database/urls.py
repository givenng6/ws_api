"""
List of all the databse routes...
"""
from django.contrib import admin
from django.urls import path
from database import users
from database import subscription
from database import bus_services
from database import dining_services

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
]

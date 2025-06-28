from django.contrib import admin
from .models import Flight, Passenger, Service

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_number", "departure_airport", "arrival_airport", "status")

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "flight", "travel_class")
    search_fields = ("first_name", "last_name", "passport_number")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service_type", "flight", "status", "service_time")
    list_filter = ("status", "service_type")

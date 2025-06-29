from rest_framework import serializers
from .models import Passenger, Flight, Service

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

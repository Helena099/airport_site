from django import forms
from .models import Passenger, Flight, Service

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = "__all__"

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = "__all__"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

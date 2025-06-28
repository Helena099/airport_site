from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Passenger, Flight, Service
from .forms import PassengerForm, FlightForm, ServiceForm
from .reco import recommend_destinations

# Passengers
class PassengerList(ListView):
    model = Passenger
    paginate_by = 25

class PassengerDetail(DetailView):
    model = Passenger

class PassengerCreate(CreateView):
    model = Passenger
    form_class = PassengerForm
    success_url = reverse_lazy("passenger_list")

class PassengerUpdate(UpdateView):
    model = Passenger
    form_class = PassengerForm
    success_url = reverse_lazy("passenger_list")

class PassengerDelete(DeleteView):
    model = Passenger
    success_url = reverse_lazy("passenger_list")

# Flights
class FlightList(ListView):
    model = Flight
    paginate_by = 25

class FlightCreate(CreateView):
    model = Flight
    form_class = FlightForm
    success_url = reverse_lazy("flight_list")

class FlightUpdate(UpdateView):
    model = Flight
    form_class = FlightForm
    success_url = reverse_lazy("flight_list")

class FlightDelete(DeleteView):
    model = Flight
    success_url = reverse_lazy("flight_list")

# Services
class ServiceList(ListView):
    model = Service
    paginate_by = 25

class ServiceCreate(CreateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy("service_list")

class ServiceUpdate(UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy("service_list")

class ServiceDelete(DeleteView):
    model = Service
    success_url = reverse_lazy("service_list")

# Reco
class RecoView(TemplateView):
    template_name = "airport/reco.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pid = self.request.GET.get("passenger_id")
        context["pid"] = pid
        context["suggestions"] = recommend_destinations(pid) if pid else []
        return context

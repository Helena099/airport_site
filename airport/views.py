# from django.urls import reverse_lazy
# from django.views.generic import (
#     ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
# )
# from .models import Passenger, Flight, Service
# from .forms import PassengerForm, FlightForm, ServiceForm
# from .reco import recommend_destinations

# from django.shortcuts import redirect
# def home(request):
#     return redirect("passenger_list")

# # Passengers
# # class PassengerList(ListView):
# #     model = Passenger
# #     paginate_by = 25

# class PassengerList(ListView):
#     model = Passenger
#     paginate_by = 50
#     ordering = ["passenger_id"]          # tri stable

# class PassengerDetail(DetailView):
#     model = Passenger

# class PassengerCreate(CreateView):
#     model = Passenger
#     form_class = PassengerForm
#     success_url = reverse_lazy("passenger_list")

# class PassengerUpdate(UpdateView):
#     model = Passenger
#     form_class = PassengerForm
#     success_url = reverse_lazy("passenger_list")

# class PassengerDelete(DeleteView):
#     model = Passenger
#     success_url = reverse_lazy("passenger_list")

# # Flights
# class FlightList(ListView):
#     model = Flight
#     paginate_by = 25

# class FlightCreate(CreateView):
#     model = Flight
#     form_class = FlightForm
#     success_url = reverse_lazy("flight_list")

# class FlightUpdate(UpdateView):
#     model = Flight
#     form_class = FlightForm
#     success_url = reverse_lazy("flight_list")

# class FlightDelete(DeleteView):
#     model = Flight
#     success_url = reverse_lazy("flight_list")

# # Services
# class ServiceList(ListView):
#     model = Service
#     paginate_by = 25

# class ServiceCreate(CreateView):
#     model = Service
#     form_class = ServiceForm
#     success_url = reverse_lazy("service_list")

# class ServiceUpdate(UpdateView):
#     model = Service
#     form_class = ServiceForm
#     success_url = reverse_lazy("service_list")

# class ServiceDelete(DeleteView):
#     model = Service
#     success_url = reverse_lazy("service_list")

# # Reco
# class RecoView(TemplateView):
#     template_name = "airport/reco.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pid = self.request.GET.get("passenger_id")
#         context["pid"] = pid
#         context["suggestions"] = recommend_destinations(pid) if pid else []
#         return context


from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.views import View                 # ← pour la nouvelle list-view
from django.shortcuts import render, redirect
from pymongo import MongoClient
import os

from .models import Passenger, Flight, Service
from .forms import PassengerForm, FlightForm, ServiceForm
from .reco import recommend_destinations


# ─────────────────────────── HOME ──────────────────────────────────────────
def home(request):
    return redirect("passenger_list")


# ───────────────────────── PASSENGERS ──────────────────────────────────────
# *** NOUVELLE LISTVIEW SANS DJONGO ***
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db     = client["airport"]


class PassengerList(View):
    template_name = "airport/passenger_list.html"
    page_size     = 100   # change la taille si tu veux

    def get(self, request):
        page = int(request.GET.get("page", 1))
        skip = (page - 1) * self.page_size

        cursor = (
            db["airport_passenger"]
            .find(
                {},
                {
                    "_id": 0,
                    "passenger_id": 1,
                    "first_name": 1,
                    "last_name": 1,
                    "flight_id": 1,
                },
            )
            .skip(skip)
            .limit(self.page_size)
        )

        passengers = list(cursor)
        context = {
            "object_list": passengers,
            "page": page,
            "has_next": len(passengers) == self.page_size,
        }
        return render(request, self.template_name, context)


# Les autres vues Passenger restent identiques
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


# ─────────────────────────── FLIGHTS ───────────────────────────────────────
# class FlightList(View):
#     template_name = "airport/flight_list.html"
#     page_size     = 50

#     def get(self, request):
#         page = int(request.GET.get("page", 1))
#         skip = (page - 1) * self.page_size
#         flights = list(
#             db["airport_flight"]
#             .find({}, {"_id": 0})
#             .skip(skip)
#             .limit(self.page_size)
#         )
#         return render(request, self.template_name, {
#             "object_list": flights,
#             "page": page,
#             "has_next": len(flights) == self.page_size,
#         })

class FlightList(View):
    template_name = "airport/flight_list.html"
    page_size = 50

    def get(self, request):
        page = int(request.GET.get("page", 1))
        skip = (page - 1) * self.page_size

        cursor = (
            db["airport_flight"]
            .find({}, {"_id": 1, "flight_number": 1,
                       "departure_airport": 1, "arrival_airport": 1,
                       "status": 1})
            .skip(skip)
            .limit(self.page_size)
        )

        flights = []
        for doc in cursor:
            doc["pk"] = str(doc["_id"])          # ← utilisé dans l’URL
            flights.append(doc)

        return render(request, self.template_name, {
            "object_list": flights,
            "page": page,
            "has_next": len(flights) == self.page_size,
        })


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


# ─────────────────────────── SERVICES ──────────────────────────────────────
# class ServiceList(View):
#     template_name = "airport/service_list.html"
#     page_size     = 50

#     def get(self, request):
#         page = int(request.GET.get("page", 1))
#         skip = (page - 1) * self.page_size
#         services = list(
#             db["airport_service"]
#             .find({}, {"_id": 0})
#             .skip(skip)
#             .limit(self.page_size)
#         )
#         return render(request, self.template_name, {
#             "object_list": services,
#             "page": page,
#             "has_next": len(services) == self.page_size,
#         })
    
class ServiceList(View):
    template_name = "airport/service_list.html"
    page_size = 50

    def get(self, request):
        page = int(request.GET.get("page", 1))
        skip = (page - 1) * self.page_size

        cursor = (
            db["airport_service"]
            .find({}, {"_id": 0,      # pk = service_id
                       "service_id": 1, "service_type": 1,
                       "flight_id": 1,  "status": 1})
            .skip(skip)
            .limit(self.page_size)
        )

        services = []
        for doc in cursor:
            doc["pk"] = doc["service_id"]         # clé primaire déclarée
            services.append(doc)

        return render(request, self.template_name, {
            "object_list": services,
            "page": page,
            "has_next": len(services) == self.page_size,
        })


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


# # ─────────────────────────── RECO ──────────────────────────────────────────
# class RecoView(TemplateView):
#     template_name = "airport/reco.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pid = self.request.GET.get("passenger_id")
#         context["pid"] = pid
#         context["suggestions"] = recommend_destinations(pid) if pid else []
#         return context

from django.core.mail import send_mail
from django.conf import settings
from airport.utils import make_email_body

class RecoView(TemplateView):
    template_name = "airport/reco.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        pid = self.request.GET.get("passenger_id")
        ctx["pid"] = pid
        ctx["suggestions"] = suggestions = recommend_destinations(pid) if pid else []

        if pid and suggestions:
            # 1) récupérer nom + email
            pdoc = db["airport_passenger"].find_one(
                {"passenger_id": pid},
                {"_id": 0, "first_name": 1, "last_name": 1, "email": 1},
            )
            if pdoc:
                name  = f'{pdoc.get("first_name", "")} {pdoc.get("last_name", "")}'.strip()
                email = pdoc.get("email")

                message = make_email_body(name or pid, suggestions)
                ctx["mail_preview"] = message      # affichage dans la page

                if email:  # 2) envoi réel via backend console/SMTP
                    send_mail(
                        subject="Vos destinations recommandées ✈️",
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL or "no-reply@airport.com",
                        recipient_list=[email],
                        fail_silently=True,        # évite un crash si SMTP off
                    )
        return ctx

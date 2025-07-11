from django.urls import path, include
from . import views

urlpatterns = [
    # — Page d’accueil : redirige vers la liste des passagers —
    path("", views.home, name="home"),

    # Passengers
    path("passengers/", views.PassengerList.as_view(), name="passenger_list"),
    path("passengers/add/", views.PassengerCreate.as_view(), name="passenger_add"),
    path("passengers/<pk>/", views.PassengerDetail.as_view(), name="passenger_detail"),
    path("passengers/<pk>/edit/", views.PassengerUpdate.as_view(), name="passenger_edit"),
    path("passengers/<pk>/delete/", views.PassengerDelete.as_view(), name="passenger_delete"),

    # Flights
    path("flights/", views.FlightList.as_view(), name="flight_list"),
    path("flights/add/", views.FlightCreate.as_view(), name="flight_add"),
    path("flights/<pk>/edit/", views.FlightUpdate.as_view(), name="flight_edit"),
    path("flights/<pk>/delete/", views.FlightDelete.as_view(), name="flight_delete"),

    # Services
    path("services/", views.ServiceList.as_view(), name="service_list"),
    path("services/add/", views.ServiceCreate.as_view(), name="service_add"),
    path("services/<pk>/edit/", views.ServiceUpdate.as_view(), name="service_edit"),
    path("services/<pk>/delete/", views.ServiceDelete.as_view(), name="service_delete"),

    # Recommandations
    path("reco/", views.RecoView.as_view(), name="reco"),

    path("api/", include("airport.api_urls")),
]

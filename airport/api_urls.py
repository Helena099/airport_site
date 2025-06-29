from rest_framework.routers import DefaultRouter
from .api_views import PassengerViewSet, FlightViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r"passengers", PassengerViewSet)
router.register(r"flights", FlightViewSet)
router.register(r"services", ServiceViewSet)

urlpatterns = router.urls

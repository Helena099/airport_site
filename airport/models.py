from djongo import models

class Flight(models.Model):
    flight_id = models.CharField(max_length=32, unique=True)
    flight_number = models.CharField(max_length=32)
    departure_airport = models.CharField(max_length=64)
    arrival_airport = models.CharField(max_length=64)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(max_length=32)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.flight_number

class Passenger(models.Model):
    passenger_id = models.CharField(max_length=32, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    passport_number = models.CharField(max_length=32)
    booking_date = models.DateField()
    destination = models.CharField(max_length=64)
    travel_class = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Service(models.Model):
    service_id = models.CharField(max_length=32, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=64)
    service_time = models.DateTimeField()
    status = models.CharField(max_length=32)

    def __str__(self):
        return self.service_type

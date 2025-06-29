# from djongo import models

# class Flight(models.Model):
#     flight_id = models.CharField(max_length=32, unique=True)
#     flight_number = models.CharField(max_length=32)
#     departure_airport = models.CharField(max_length=64)
#     arrival_airport = models.CharField(max_length=64)
#     departure_time = models.DateTimeField()
#     arrival_time = models.DateTimeField()
#     status = models.CharField(max_length=32)
#     capacity = models.PositiveIntegerField()

#     def __str__(self):
#         return self.flight_number

# class Passenger(models.Model):
#     passenger_id = models.CharField(max_length=32, unique=True)
#     flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True)
#     first_name = models.CharField(max_length=64)
#     last_name = models.CharField(max_length=64)
#     passport_number = models.CharField(max_length=32)
#     booking_date = models.DateField()
#     destination = models.CharField(max_length=64)
#     travel_class = models.CharField(max_length=32)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class Service(models.Model):
#     service_id = models.CharField(max_length=32, unique=True)
#     flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
#     service_type = models.CharField(max_length=64)
#     service_time = models.DateTimeField()
#     status = models.CharField(max_length=32)

#     def __str__(self):
#         return self.service_type


from djongo import models


# ──────────────────── FLIGHT ─────────────────────────────────────────────
class Flight(models.Model):
    flight_number     = models.CharField(max_length=32, unique=True)   # ex: FL00001
    departure_airport = models.CharField(max_length=64)
    arrival_airport   = models.CharField(max_length=64)
    departure_time    = models.DateTimeField()
    arrival_time      = models.DateTimeField()
    status            = models.CharField(max_length=32)
    capacity          = models.PositiveIntegerField()

    class Meta:
        db_table = "airport_flight"

    def __str__(self):
        return self.flight_number


# ──────────────────── PASSENGER ──────────────────────────────────────────
class Passenger(models.Model):
    # _id = ObjectId() géré par Djongo ⇒ on garde la PK par défaut
    passenger_id     = models.CharField(max_length=32, unique=True)
    flight           = models.ForeignKey(
        Flight,
        to_field="flight_number",          # FK via le champ texte
        db_column="flight_id",
        on_delete=models.SET_NULL,
        null=True,
    )
    first_name       = models.CharField(max_length=64)
    last_name        = models.CharField(max_length=64)
    passport_number  = models.CharField(max_length=32)
    booking_date     = models.DateField()
    destination      = models.CharField(max_length=64)
    travel_class     = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = "airport_passenger"
        # ordering  = ["passenger_id"]       # tri stable pour la pagination

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ──────────────────── SERVICE ────────────────────────────────────────────
class Service(models.Model):
    service_id   = models.CharField(max_length=32, primary_key=True)
    flight       = models.ForeignKey(
        Flight,
        to_field="flight_number",
        db_column="flight_id",
        on_delete=models.CASCADE,
        related_name="services",
    )
    service_type = models.CharField(max_length=64)
    service_time = models.DateTimeField()
    status       = models.CharField(max_length=32)

    class Meta:
        db_table = "airport_service"

    def __str__(self):
        return self.service_type

from django.db import models

# Create your models here.
class Line(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    direction_destinations = models.JSONField()
    direction_names = models.JSONField()
    line = models.CharField(max_length=255)
    polylines = models.JSONField()

    def __str__(self):
        return self.name

class Stop(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    location = models.JSONField()
    municipality = models.CharField(max_length=255)
    street = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Train(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    line = models.JSONField() 
    location = models.JSONField()
    status = models.CharField(max_length=255, null=True)
    stop = models.JSONField(null=True)
    trip = models.CharField(max_length=255, null=True)
    occupancy = models.CharField(max_length=255, null=True)
    speed = models.FloatField(null=True)
    direction_id = models.IntegerField(null=True)
    last_update = models.DateTimeField()

    def __str__(self):
        return self.id

class Prediction(models.Model):
    id = models.AutoField(primary_key=True)
    trip_id = models.CharField(max_length=255, null=True)
    vehicle_id = models.CharField(max_length=255, null=True)
    stop_id = models.CharField(max_length=255, null=True)
    arrival_time = models.CharField(max_length=255, null=True)
    departure_time = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.trip_id + self.vehicle_id + self.stop_id

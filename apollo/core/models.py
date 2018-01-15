from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#todo: how to model room availability?
#we could keep things simple by just using a boolean
#but it would require frequent access to keep things updated
class Room(models.Model):
    display_name = models.CharField(max_length=50)
    location_string = models.CharField(max_length=50)
    lat_long = models.CharField(max_length=50)
    capacity = models.SmallIntegerField(default=1)
    #stored as a string that will be encoded/decoded as a json list for now
    tags = models.TextField(null=True, default="[]")

class RoomData(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temp = models.FloatField()
    noise = models.FloatField()
    occupied = models.BooleanField()
    headcount = models.SmallIntegerField()

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #reserved_by = # todo: user as foreign key
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        #could just do this validation on the frontend as well
        if self.end_time < self.begin_time:
            print("Error creating reservation where end time is before begin time")
            return
        else:
            super().save(*args, **kwargs)

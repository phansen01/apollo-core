from django.db import models

# Create your models here.
class Room(models.Model):
    display_name = models.CharField(max_length=50)
    location_string = models.CharField(max_length=50)
    lat_long = models.CharField(max_length=50)

class RoomData(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temp = models.FloatField()
    noise = models.FloatField()
    occupied = models.BooleanField()
    headcount = models.SmallIntegerField()
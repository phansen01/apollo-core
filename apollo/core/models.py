from django.db import models

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
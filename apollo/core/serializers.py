from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apollo.core.models import Room, RoomData, Reservation
from django.db.models import Q

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'display_name', 'location_string', 'lat_long', 'capacity', 'tags')

class RoomDataSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = RoomData
        fields = ('room', 'timestamp', 'temp', 'noise', 'occupied', 'headcount')

class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    def validate(self, data):
        """
        Check that a reservation is valid (doesn't overlap existing reservations)
        """
        if data['begin_time'] > data['end_time']:
            raise serializers.ValidationError("End time must be after begin time")
        
        #There are 3 cases to check to find an overlap:
        #1) the meeting begins before this meeting, and ends after this one begins
        #2) the meeting starts before this one ends, and ends before this one ends
        #3) the meeting starts after this one, and ends before this one ends
        overlaps = Reservation.objects.filter(
            room=data['room']
        ).filter(
            Q(begin_time__lte=data['begin_time'], end_time__gt=data['begin_time']) |
            Q(begin_time__lt=data['end_time'], end_time__gte=data['end_time']) |
            Q(begin_time__gte=data['begin_time'], end_time__lte=data['end_time'])
        )

        if overlaps.exists():
            raise serializers.ValidationError("This reservation overlaps existing reservation(s)")
        
        return data

    class Meta:
        model = Reservation
        fields = ('id', 'room', 'begin_time', 'end_time')

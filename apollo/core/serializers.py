from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apollo.core.models import Room, RoomData

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

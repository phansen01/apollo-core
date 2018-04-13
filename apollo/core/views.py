from datetime import datetime, timedelta
from django.utils import dateparse
from django.shortcuts import render
from django.db.models import Q, Count
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apollo.core.serializers import (UserSerializer, GroupSerializer,
    RoomSerializer, RoomDataSerializer, ReservationSerializer)
from apollo.core.models import Room, RoomData, Reservation
from apollo.core.permissions import permissions
from apollo.core.permissions import IsOwnerOrReadOnly
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class GhostedMeetings(APIView):
    def get(self, request):
        room = int(request.query_params.get('room', 0))
        #begin = request.query_params.get('startTime', '')
        #end = request.query_params.get('endTime', '')
        
        result = {}
        rooms = Room.objects.all()
        if room != 0:
            rooms = Room.objects.filter(pk=room)
        for room in rooms:
            result[room.id] = 0
            today = datetime.today()
            a_week_ago = today - timedelta(days=7)
            reservations = Reservation.objects.filter(room=room).filter(
                Q(begin_time__gte=a_week_ago) &
                Q(begin_time__lte=today)
            )
            for reservation in reservations:
                #get all roomdata that we have which overlaps the reservation
                data = RoomData.objects.filter(room=room).filter(
                    Q(timestamp__gte=reservation.begin_time) &
                    Q(timestamp__lte=reservation.end_time)
                )
                #if the room was ever occupied, dont count this meeting
                #as ghosted. Otherwise, increment the number of ghosted
                #meetings for this room.
                ghosted = True
                for d in data:
                    if d.occupied:
                        ghosted = False
                        break
                if ghosted:
                    result[room.id] += 1
        return JsonResponse(result)

class ReservationsPerWeek(APIView):
    def get(self, request):
        room = int(request.query_params.get('room', 0))
        #begin = request.query_params.get('startTime', '')
        #end = request.query_params.get('endTime', '')
        
        result = {}
        rooms = Room.objects.all()
        if room != 0:
            rooms = Room.objects.filter(pk=room)
        for room in rooms:
            result[room.id] = {}
            result[room.id]["display_name"] = room.display_name
            today = datetime.today()
            a_week_ago = today - timedelta(days=7)
            weekly_reservations = Reservation.objects.filter(room=room).filter(
                Q(begin_time__gte=a_week_ago) &
                Q(begin_time__lte=today)
            )
            num_reservations = weekly_reservations.count()
            total_usage_mins = 0
            for res in weekly_reservations:
                length = res.end_time - res.begin_time
                total_usage_mins += length.seconds / 60
            result[room.id]["total_usage_mins"] = int(total_usage_mins)
            result[room.id]["num_reservations"] = num_reservations

        return JsonResponse(result)

class BusiestTimes(APIView):
    def get(self, request):
        room = int(request.query_params.get('room', 0))
        #begin = request.query_params.get('startTime', '')
        #end = request.query_params.get('endTime', '')
        
        result = {}
        rooms = Room.objects.all()
        if room != 0:
            rooms = Room.objects.filter(pk=room)
        for room in rooms:
            result[room.id] = {}
            result[room.id]["display_name"] = room.display_name
            result[room.id]["hourly_reservations"] = {hour: 0 for hour in range(24)}
            today = datetime.today()
            a_week_ago = today - timedelta(days=7)
            weekly_reservations = Reservation.objects.filter(room=room).filter(
                Q(begin_time__gte=a_week_ago) &
                Q(begin_time__lte=today)
            )
            for reservation in weekly_reservations:
                hour = reservation.begin_time.hour
                result[room.id]["hourly_reservations"][hour] += 1
        return JsonResponse(result)

class RoomDataView(generics.ListCreateAPIView):
    """
    View to list or update room data points for a given room
    """
    queryset = RoomData.objects.all()
    serializer_class = RoomDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        room = int(request.query_params.get('room', 0))
        begin = request.query_params.get('startTime', '')
        end = request.query_params.get('endTime', '')

        matches = RoomData.objects.all()
        if room != 0:
            matches = RoomData.objects.filter(room=room)
        if begin != '' and end != '':
            begin_time = dateparse.parse_datetime(begin)
            end_time = dateparse.parse_datetime(end)
            matches = matches.filter(
                Q(timestamp__gte=begin_time) &
                Q(timestamp__lte=end_time)
            )
        
        serializer = RoomDataSerializer(list(matches), many=True)
        return Response(serializer.data)

class MatchingRooms(APIView):
    """
    View to return all rooms matching the search criteria
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        capacity = int(request.query_params.get('capacity', 0))
        tags = request.query_params.getlist('tags', [])
        #todo: decide on a design for default/missing start/end time
        begin = request.query_params.get('startTime', '')
        end = request.query_params.get('endTime', '')

        begin_time = dateparse.parse_datetime(begin)
        end_time = dateparse.parse_datetime(end)

        #todo: sort of duplicate logic here and in the Reservation
        #serializer, should try to refactor
        overlaps = Reservation.objects.filter(
            Q(begin_time__lte=begin_time, end_time__gt=begin_time) |
            Q(begin_time__lt=end_time, end_time__gte=end_time) |
            Q(begin_time__gte=begin_time, end_time__lte=end_time)
        )
        print(overlaps)
        rooms_to_exclude = set([overlap.room.id for overlap in overlaps])

        if rooms_to_exclude:
            print("Rooms to exclude: {}".format(rooms_to_exclude))
        #todo: right now tag matches are done based on subsets
        #(i.e. room has at least all requested features). Should
        #make this more robust by implementing partial matches
        rooms = list(Room.objects.all())
        matches = []

        for room in rooms:
            if room.id in rooms_to_exclude:
                print("Room {} has an overlapping reservation, skipping.".format(room.id))
                continue
            room_tags = room.tags
            print("actual: {}".format(room_tags))
            print("desired: {}".format(tags))
            if (room.capacity >= capacity
                    and (set(room_tags) >= set(tags))):
                matches.append(room)

        print(matches)
        serializer = RoomSerializer(matches, many=True)
        return Response(serializer.data)

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View for fetching, updating, or deleting an existing room
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ReservationList(generics.ListCreateAPIView):
    """
    View for fetching all reservations or adding a reservation
    """
    #todo: will need to add object ownership to reservation instances so that
    #IsOwnerOrReadOnly is actually effective.

    #todo: also will need to think about whether it's ok for users to lose
    #the ability to modify their reservation if they reserve anonymously, or
    #find a workaround for this.

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ReservationDetail(generics.RetrieveDestroyAPIView):
    """
    View for fetching a reservation or deleting it
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
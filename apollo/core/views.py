from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apollo.core.serializers import (UserSerializer, GroupSerializer,
    RoomSerializer, RoomDataSerializer)
from apollo.core.models import Room, RoomData
from apollo.core.permissions import permissions
from apollo.core.permissions import IsOwnerOrReadOnly
import json
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

class RoomData(generics.ListCreateAPIView):
    """
    View to list or update room data points for a given room
    """
    queryset = RoomData.objects.all()
    serializer_class = RoomDataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class MatchingRooms(APIView):
    """
    View to return all rooms matching the search criteria
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        capacity = int(request.query_params.get('capacity', 0))
        tags = request.query_params.getlist('tags', [])
        #todo: decide on a design for default/missing start/end time
        start = request.query_params.get('startTime', 0)
        end = request.query_params.get('endTime', 0)

        json_dec = json.decoder.JSONDecoder()

        #todo: right now tag matches are done based on subsets
        #(i.e. room has at least all requested features). Should
        #make this more robust by implementing partial matches
        rooms = [room for room in Room.objects.all()]
        matches = []

        for room in rooms:
            room_tags = json_dec.decode(room.tags)
            print("actual: {}".format(room_tags))
            print("desired: {}".format(tags))
            if (room.capacity >= capacity
                    and (set(room_tags) >= set(tags))):
                matches.append(room)

        print(matches)
        serializer = RoomSerializer(matches, many=True)
        return Response(serializer.data)

class RoomDetail(APIView):
    """
    todo
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, id):
        try:
            room = Room.objects.get(id=id)
            return Response(RoomSerializer(room).data)
        except Room.DoesNotExist:
            print("No room with id {} exists".format(id))
            #todo return error

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apollo.core.serializers import (UserSerializer, GroupSerializer,
    RoomSerializer, RoomDataSerializer)
from apollo.core.models import Room, RoomData
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

#todo view for RoomData
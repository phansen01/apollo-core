#Views intended to be used for management by e.g. AppEngine cron.yaml
from datetime import datetime, timedelta
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Avg
from apollo.core.models import Room, RoomData, Reservation

NOISE_THRESHOLD = 50 #todo: set this to something meaningful

class UpdateDynamicTags(APIView):
    def get(self, request):
        for room in Room.objects.all():
            today = datetime.today()
            a_week_ago = today - timedelta(days=7)
            avg_noise = RoomData.objects.filter(room=room).filter(
                    Q(timestamp__gte=a_week_ago) &
                    Q(timestamp__lte=today)
            ).aggregate(Avg('noise')).get('noise__avg')
            if avg_noise >= NOISE_THRESHOLD:
                if 'quiet' in room.tags:
                    room.tags.remove('quiet')
            else:
                room.tags.append('quiet')
            room.save()
            return Response(status=200)
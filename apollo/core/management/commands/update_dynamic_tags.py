from django.core.management.base import BaseCommand, CommandError
from apollo.core.models import Room, RoomData
from datetime import datetime, timedelta
from django.db.models import Avg, Q

NOISE_THRESHOLD = 50 #todo: no idea what this should be.

class Command(BaseCommand):
    help = 'Update dynamic tags for rooms'

    
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
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

        self.stdout.write(self.style.SUCCESS('Successfully updated tags'))
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from apollo.core.models import Room, RoomData, Reservation
from random import choice, randrange

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('room', nargs=1, type=int)

    def handle(self, *args, **options):
        today = datetime.today()
        a_week_ago = today - timedelta(days=7)
        hours = 7 * 24
        #A list of each hour in between a week ago and today
        dates = [a_week_ago + timedelta(hours=x) for x in range(hours+1)]

        room = Room.objects.get(pk=options['room'][0])
        for d in dates:
            #create a reservation on ~85% of possible times
            if randrange(0, 101) >= 85:
                continue
            duration = choice([15, 30, 45])
            ghosted = False
            #~15% of meetings are ghosted
            if randrange(0, 101) <= 15:
                ghosted = True
            res = Reservation(
                room=room,
                begin_time=d,
                end_time=d+timedelta(minutes=duration)
            )
            res.save()
            if ghosted:
                #create a data point for this meeting that shows no occupancy
                data = RoomData(
                    room=room,
                    timestamp=d+timedelta(minutes=1),
                    temp=randrange(67, 82),
                    noise=randrange(30, 55),
                    occupied=False,
                    headcount=0
                )
                data.save()
            else:
                data = RoomData(
                    room=room,
                    timestamp=d+timedelta(minutes=1),
                    temp=randrange(67, 82),
                    noise=randrange(30, 55),
                    occupied=True,
                    headcount=1
                )
                data.save()
                
            
from django.conf.urls import url
from apollo.core import views

urlpatterns = [
    url(r'^api/rooms/$', views.RoomList.as_view()),
    url(r'^api/search/$', views.MatchingRooms.as_view())
]
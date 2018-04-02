from django.conf.urls import url, re_path, include
from django.urls import path
from apollo.core import views
from apollo.core import models

urlpatterns = [
    url(r'^rooms/$', views.RoomList.as_view()),
    url(r'^search/$', views.MatchingRooms.as_view()),
    re_path(r'^rooms/(?P<pk>[0-9]+)/$', views.RoomDetail.as_view()),
    url(r'^roomdata/$', views.RoomDataView.as_view()),
    url(r'^reservations/$', views.ReservationList.as_view()),
    re_path(r'^reservations/(?P<pk>[0-9]+)/$', views.ReservationDetail.as_view()),
    url(r'^ghosted-meetings/$', views.GhostedMeetings.as_view()),
    url(r'^reservations-per-week/$', views.ReservationsPerWeek.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
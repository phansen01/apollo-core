from django.conf.urls import url, re_path, include
from django.urls import path
from apollo.core import views
from apollo.core import models

urlpatterns = [
    url(r'^api/rooms/$', views.RoomList.as_view()),
    url(r'^api/search/$', views.MatchingRooms.as_view()),
    re_path(r'^api/rooms/(?P<pk>[0-9]+)/$', views.RoomDetail.as_view()),
    url(r'^api/roomdata/$', views.RoomDataView.as_view()),
    url(r'^api/reservations/$', views.ReservationList.as_view()),
    re_path(r'^api/reservations/(?P<pk>[0-9]+)/$', views.ReservationDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
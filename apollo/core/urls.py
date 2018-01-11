from django.conf.urls import url
from django.urls import path
from apollo.core import views

urlpatterns = [
    url(r'^api/rooms/$', views.RoomList.as_view()),
    url(r'^api/search/$', views.MatchingRooms.as_view()),
    path('api/rooms/<int:id>', views.RoomDetail.as_view())
]
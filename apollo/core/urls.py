from django.conf.urls import url
from apollo.core import views

urlpatterns = [
    url(r'^rooms/$', views.RoomList.as_view())
]
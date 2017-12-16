from django.conf.urls import url
from apollo.core import views

urlpatterns = [
    url(r'^rooms/$', views.room_list)
]
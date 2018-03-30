from django.conf.urls import url, re_path, include
from django.urls import path
from apollo.core.management import views

urlpatterns = [
    url(r'^update-dynamic-tags/$', views.UpdateDynamicTags.as_view()),
]
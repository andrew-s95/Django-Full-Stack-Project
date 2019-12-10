from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^shows/new$', views.add_show_page),
    url(r'^shows/create$', views.add_show),
    url(r'^shows/(?P<num>\d+)$', views.view_show),
    url(r'^shows/(?P<num>\d+)/edit$', views.edit_show_page),
    url(r'^shows/(?P<num>\d+)/edit/process$', views.edit_show),
    url(r'^shows/(?P<num>\d+)/delete$', views.remove_show),
    url(r'^$', views.index),
    url(r'^shows$', views.index),
]


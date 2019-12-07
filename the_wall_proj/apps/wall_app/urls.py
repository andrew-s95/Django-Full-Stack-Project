from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.register),
    url(r'^login$', views.login),
    url(r'^wall$', views.wall),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment$', views.post_comment),
    url(r'^message/delete/(?P<num>\d+)$', views.delete_message),
    url(r'^logout$', views.logout),
]
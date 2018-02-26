from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),  #this goes to localhost:8000/users
    url(r'^add$', views.add),
    url(r'^courses/destroy/(?P<id>\d+)$', views.destroy),
    url(r'^goback$', views.go_back),
    url(r'^(?P<id>\d+)/remove$', views.remove),
]
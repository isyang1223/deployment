from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),  #this goes to localhost:8000/users
    url(r'^/success$', views.success),
    url(r'^/login$', views.login),
    url(r'^/registration$', views.registration),
    url(r'^/additem$', views.additem),
    url(r'^/create$', views.createitem),
    url(r'^/logout$', views.logout),
    url(r'^/(?P<id>\d+)$', views.showitem), 
    url(r'^/remove/(?P<id>\d+)$', views.removeitem), 
    url(r'^/add/(?P<id>\d+)$', views.addtowishlist), 
    url(r'^/delete/(?P<id>\d+)$', views.delete), 
]
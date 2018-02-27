from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),  #this goes to localhost:8000/users
    url(r'^/success$', views.success),
    url(r'^/login$', views.login),
    url(r'^/registration$', views.registration),
    url(r'^/logout$', views.logout),
]
from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login_action'),
]

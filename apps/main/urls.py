from django.conf.urls import url, include
from django.core.urlresolvers import reverse

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'add$', views.add, name = 'add'),
    url(r'edit/(?P<id>\d+)$', views.edit, name= 'edit'),
    url(r'editAppointment/(?P<id>\d+)$', views.editAppointment, name= 'editAppointment'),
    url(r'delete/(?P<id>\d+)$', views.delete, name = 'delete'),
    url(r'logout$', views.logout, name = 'logout')
]

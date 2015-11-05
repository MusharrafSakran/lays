__author__ = 'MUSHARRAF'
from django.conf.urls import include, url
from public import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
]

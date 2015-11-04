__author__ = 'MUSHARRAF'
from django.conf.urls import include, url
from api import views
from django.contrib import admin

urlpatterns = [
    url(r'^validate-iban/$', views.ValidateIBAN.as_view()),
]

from django.conf.urls import url
from api import views

__author__ = 'MUSHARRAF'

urlpatterns = [
    url(r'^validate-iban/$', views.validate_iban_view),
    url(r'^validate-mobile-number/$', views.validate_mobile_number_view),
]

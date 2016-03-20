from django.conf.urls import url
from api import views

__author__ = 'MUSHARRAF'

urlpatterns = [
    url(r'^validate-iban/$', views.validate_iban_view),
    url(r'^validate-mobile-number/$', views.validate_mobile_number_view),
    url(r'^convert-greg-to-hijri/$', views.convert_greg_to_hijri_view),
    url(r'^convert-hijri-to-greg/$', views.convert_hijri_to_greg_view),
    url(r'^get-hijri-month-length/$', views.get_hijri_month_length_view),
    url(r'^get-today-date/$', views.get_today_date_view),
    url(r'^validate-identity/$', views.validate_id_view),
    # url(r'^test-sms/$', views.test_sms_view),
]

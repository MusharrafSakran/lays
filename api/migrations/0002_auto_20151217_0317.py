# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_endpoints(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Endpoint = apps.get_model("api", "Endpoint")
    Endpoint.objects.create(name='validate_iban_view')
    Endpoint.objects.create(name='validate_mobile_number_view')
    Endpoint.objects.create(name='convert_greg_to_hijri_view')
    Endpoint.objects.create(name='convert_hijri_to_greg_view')
    Endpoint.objects.create(name='get_hijri_month_length_view')
    Endpoint.objects.create(name='get_today_date_view')
    Endpoint.objects.create(name='validate_id_view')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_endpoints),
    ]

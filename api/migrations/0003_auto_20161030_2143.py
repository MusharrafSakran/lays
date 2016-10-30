# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def create_endpoints(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Endpoint = apps.get_model("api", "Endpoint")
    Endpoint.objects.create(name='validate_disposable_email_view')

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151217_0317'),
    ]

    operations = [
        migrations.RunPython(create_endpoints),
    ]

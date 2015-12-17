from django.contrib import admin

# Register your models here.
from .models import Endpoint


class EndpointAdmin(admin.ModelAdmin):
    fields = ['name', 'hits']
    list_display = ('name', 'hits', )

admin.site.register(Endpoint, EndpointAdmin)

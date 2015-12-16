from django.contrib import admin

# Register your models here.
from .models import Subscribers


class SubscribersAdmin(admin.ModelAdmin):
    fields = ['email']
    list_display = ('pk', 'email', )

admin.site.register(Subscribers, SubscribersAdmin)

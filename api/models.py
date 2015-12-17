from django.db import models

# Create your models here.


class Endpoint(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hits = models.BigIntegerField(default=0)

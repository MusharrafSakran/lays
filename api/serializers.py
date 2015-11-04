__author__ = 'MUSHARRAF'
from rest_framework import serializers


class IBANSerializer(serializers.Serializer):
    class Meta:
        fields = ('number', 'status')

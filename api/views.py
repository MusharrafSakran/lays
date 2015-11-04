from api.serializers import IBANSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
# Create your views here.
from api.utils import validate_iban, detect_iban_bank


class ValidateIBAN(APIView):
    def post(self, request):
        iban = request.data['number']
        return Response({'number': request.data['number'], 'valid': validate_iban(iban), 'bank': detect_iban_bank(iban)})

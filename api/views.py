# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from api.utils import validate_iban, detect_iban_bank, validate_mobile_number


@api_view(["POST"])
def validate_iban_view(request):
    """
    Validate ANY Saudi IBAN
    ---
    # YAML (must be separated by `---`)

    type:
      number:
        required: true
        type: string
      valid:
        required: true
        type: boolean
      bank:
        required: true
        type: string
      bank_ar:
        required: true
        type: string


    omit_serializer: true

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: number
          description: IBAN number
          required: true
          type: string
          paramType: form

    responseMessages:
        - code: 400
          message: IBAN is not provided
        - code: 429
          message: Client has been throttled by exceeding daily limit (175 requests/day)
    """
    if 'number' not in request.data:
        return Response({'message': 'IBAN is not provided'}, status.HTTP_400_BAD_REQUEST)
    iban = request.data['number']
    iban_valid = validate_iban(iban)
    return Response(
        {'number': request.data['number'], 'valid': iban_valid,
         'bank': detect_iban_bank(iban)[0] if iban_valid is True else '',
         'bank_ar': detect_iban_bank(iban)[1].decode('utf-8') if iban_valid is True else ''})


@api_view(["POST"])
def validate_mobile_number_view(request):
    """
    Validate ANY Saudi Mobile Number
    ---
    # YAML (must be separated by `---`)

    type:
      number:
        required: true
        type: string
      valid:
        required: true
        type: boolean


    omit_serializer: true

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: number
          description: mobile number
          required: true
          type: string
          paramType: form

    responseMessages:
        - code: 400
          message: mobile number is not provided
        - code: 429
          message: Client has been throttled by exceeding daily limit (175 requests/day)
    """
    if 'number' not in request.data:
        return Response({'message': 'mobile number is not provided'}, status.HTTP_400_BAD_REQUEST)
    number = request.data['number']
    return Response(
        {'number': request.data['number'], 'valid': validate_mobile_number(number)})

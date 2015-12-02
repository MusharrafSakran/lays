# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from api.utils import validate_iban, detect_iban_bank, validate_mobile_number, convert_greg_to_hijri, \
    convert_hijri_to_greg, get_hijri_month_length, get_today_date


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


@api_view(["POST"])
def convert_greg_to_hijri_view(request):
    """
    Convert Gregorian date to Hijri (Umm-alqura) date
    ---
    # YAML (must be separated by `---`)

    type:
      day_name:
        required: true
        type: string
      month_name:
        required: true
        type: string
      day:
        required: true
        type: integer
      month:
        required: true
        type: integer
      year:
        required: true
        type: integer
      day_name_en:
        required: true
        type: string
      month_name_gr:
        required: true
        type: string
      day_gr:
        required: true
        type: integer
      month_gr:
        required: true
        type: integer
      year_gr:
        required: true
        type: integer
      month_len:
        required: true
        type: integer


    omit_serializer: true

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: day
          description: gregorian date day, 0 < day < 32
          required: true
          type: string
          paramType: form
        - name: month
          description: gregorian date month, 0 < month < 13
          required: true
          type: string
          paramType: form
        - name: year
          description: gregorian date year, 2030 > year > 1899
          required: true
          type: string
          paramType: form

    responseMessages:
        - code: 400
          message: given date is not complete
        - code: 400
          message: given date values are incorrect
        - code: 400
          message: given date is out of supported range
        - code: 429
          message: Client has been throttled by exceeding daily limit (175 requests/day)
    """

    if 'day' and 'month' and 'year' not in request.data:
        return Response({'message': 'given date is not complete'}, status.HTTP_400_BAD_REQUEST)
    year = 0
    try:
        day = int(request.data['day'])
        month = int(request.data['month'])
        year = int(request.data['year'])
        if not 2030 > year > 1899:
            raise IndexError
        date = convert_greg_to_hijri(day, month, year)
    except ValueError as e:
        if e.message == 'year=' + str(year) + ' is before 1900; the datetime strftime() methods require year >= 1900':
            return Response({'message': 'given date is out of supported range'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'given date values are incorrect'}, status.HTTP_400_BAD_REQUEST)
    except IndexError:
        return Response({'message': 'given date is out of supported range'}, status.HTTP_400_BAD_REQUEST)
    return Response(date.__dict__)


@api_view(["POST"])
def convert_hijri_to_greg_view(request):
    """
    Convert Hijri (Umm-alqura) date to Gregorian date
    ---
    # YAML (must be separated by `---`)

    type:
      day_name:
        required: true
        type: string
      month_name:
        required: true
        type: string
      day:
        required: true
        type: integer
      month:
        required: true
        type: integer
      year:
        required: true
        type: integer
      day_name_en:
        required: true
        type: string
      month_name_gr:
        required: true
        type: string
      day_gr:
        required: true
        type: integer
      month_gr:
        required: true
        type: integer
      year_gr:
        required: true
        type: integer


    omit_serializer: true

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: day
          description: hijri date day, 0 < day < 31
          required: true
          type: string
          paramType: form
        - name: month
          description: hijri date month, 0 < month < 13
          required: true
          type: string
          paramType: form
        - name: year
          description: hijri date year, 1356 < year < 1450
          required: true
          type: string
          paramType: form

    responseMessages:
        - code: 400
          message: given date is not complete
        - code: 400
          message: given date values are incorrect
        - code: 400
          message: given date is out of supported range
        - code: 429
          message: Client has been throttled by exceeding daily limit (175 requests/day)
    """

    if 'day' and 'month' and 'year' not in request.data:
        return Response({'message': 'given date is not complete'}, status.HTTP_400_BAD_REQUEST)
    try:
        day = int(request.data['day'])
        month = int(request.data['month'])
        year = int(request.data['year'])
        if not 1356 < year < 1450:
            raise IndexError
        date = convert_hijri_to_greg(day, month, year)
    except ValueError:
        return Response({'message': 'given date values are incorrect'}, status.HTTP_400_BAD_REQUEST)
    except IndexError:
        return Response({'message': 'given date is out of supported range'}, status.HTTP_400_BAD_REQUEST)
    return Response(date.__dict__)


@api_view(["POST"])
def get_hijri_month_length_view(request):
    """
    get length for a given Hijri (Umm-alqura) month
    ---
    # YAML (must be separated by `---`)

    type:
      month_length:
        required: true
        type: integer


    omit_serializer: true

    parameters_strategy: merge
    omit_parameters:
        - path
    parameters:
        - name: month
          description: hijri date month, 0 < month < 13
          required: true
          type: string
          paramType: form
        - name: year
          description: hijri date year, 1356 < year < 1450
          required: true
          type: string
          paramType: form

    responseMessages:
        - code: 400
          message: given date is not complete
        - code: 400
          message: given date values are incorrect
        - code: 400
          message: given date is out of supported range
        - code: 429
          message: Client has been throttled by exceeding daily limit (175 requests/day)
    """

    if 'month' and 'year' not in request.data:
        return Response({'message': 'given date is not complete'}, status.HTTP_400_BAD_REQUEST)
    try:
        month = int(request.data['month'])
        year = int(request.data['year'])
        if not 1356 < year < 1450:
            raise IndexError
        month_length = get_hijri_month_length(month, year)
    except ValueError:
        return Response({'message': 'given date values are incorrect'}, status.HTTP_400_BAD_REQUEST)
    except IndexError:
        return Response({'message': 'given date is out of supported range'}, status.HTTP_400_BAD_REQUEST)
    return Response({'month_length': month_length})


@api_view(["GET"])
def get_today_date_view(request):
    """
    get today date in both Hijri (Umm-alqura) and Gregorian flavors
    ---
    # YAML (must be separated by `---`)

    type:
      day_name:
        required: true
        type: string
      month_name:
        required: true
        type: string
      day:
        required: true
        type: integer
      month:
        required: true
        type: integer
      year:
        required: true
        type: integer
      day_name_en:
        required: true
        type: string
      month_name_gr:
        required: true
        type: string
      day_gr:
        required: true
        type: integer
      month_gr:
        required: true
        type: integer
      year_gr:
        required: true
        type: integer
      month_len:
        required: true
        type: integer


    omit_serializer: true

    parameters_strategy: merge
    omit_parameters:
        - path

    responseMessages:
        - code: 429
          message: Client has been throttled by exceeding daily limit (175 requests/day)
    """

    return Response(get_today_date().__dict__)

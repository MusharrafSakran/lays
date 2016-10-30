# -*- coding: utf-8 -*-
import re
from umalqurra.hijri_date import HijriDate
import disposable_emails_list

__author__ = 'MUSHARRAF'
_country2length = dict(
    AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20, BR=29,
    BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
    FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18,
    GT=28, HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30,
    LV=21, LB=28, LI=21, LT=20, LU=20, MK=19, MT=31, MR=27,
    MU=30, MC=27, MD=24, ME=22, NL=18, NO=15, PK=24, PS=29,
    PL=28, PT=25, RO=24, SM=27, SA=24, RS=22, SK=24, SI=19,
    ES=24, SE=24, CH=21, TN=24, TR=26, AE=23, GB=22, VG=24)

_iban_banks = [
    (10, 'Alahli bank'),
    (20, 'Riyadh Bank'),
    (15, 'Albilad Bank'),
    (05, 'Alinma Bank'),
    (60, 'Aljazeera Bank'),
    (80, 'Alrajhi Bank'),
    (30, 'Alarabi Bank'),
    (76, 'Muscat Bank'),
    (85, 'BMP Parisbas Bank'),
    (81, 'Deutsche Bank'),
    (95, 'Emirates Bank International'),
    (90, 'Gulf International Bank'),
    (86, 'JPMorgan Chase Bank'),
    (71, 'National Bank of Bahrain'),
    (75, 'National Bank of Kuwait'),
    (82, 'National Bank of Pakistan'),
    (45, 'SABB'),
    (40, 'SAMBA'),
    (55, 'Saudi Fransi Bank'),
    (50, 'Saudi Hollandi Bank'),
    (65, 'Saudi Investment Bank'),
    (83, 'State Bank of India'),
    (84, 'Turkiye Cumhuriyeti Ziraat Bankasi'),
]

_iban_banks_ar = [
    (10, 'البنك الاهلي'),
    (20, 'بنك الرياض'),
    (15, 'بنك البلاد'),
    (05, 'بنك الإنماء'),
    (60, 'بنك الجزيرة'),
    (80, 'بنك الراجحي'),
    (30, 'البنك العربي'),
    (76, 'بنك مسقط'),
    (85, 'بي إم بي باريسباس'),
    (81, 'بنك دويتشه'),
    (95, 'البنك الإماراتي العالمي'),
    (90, 'البنك الخليجي العالمي'),
    (86, 'بنك جي بي مورغان تشايس'),
    (71, 'البنك الوطني البحريني'),
    (75, 'النبك الوطني الكويتي'),
    (82, 'البنك الوطني الباكستاني'),
    (45, 'ساب'),
    (40, 'سامبا'),
    (55, 'البنك السعودي الفرنسي'),
    (50, 'البنك السعودي الهولندي'),
    (65, 'البنك السعودي للإستثمار'),
    (83, 'البنك الحكومي الهندي'),
    (84, 'بنك كمهورياتي زيرات التركي'),
]

_identity_types = [
    (1, 'Saudi National ID'),
    (2, 'Non-Saudi Resident ID (Iqama)'),
]

_identity_types_ar = [
    (1, 'هوية وطنية سعودية'),
    (2, 'رقم إقامة لغير السعوديين')
]


def validate_iban(iban):
    # Ensure upper alphanumeric input.
    iban = iban.replace(' ', '').replace('\t', '')
    # if not re.match(r'^[\dA-Z]+$', iban):
    if not re.match(r'^[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}', iban):
        return False
    # Validate country code against expected length.
    if len(iban) != _country2length[iban[:2]]:
        return False
    else:
        return True
    # Shift and convert.
    # iban = iban[4:] + iban[:4]
    # digits = int(''.join(str(int(ch, 36)) for ch in iban)) #BASE 36: 0..9,A..Z -> 0..35
    # return digits % 97 == 1


def detect_iban_bank(iban):
    # bank_name = [i for i, v in enumerate(_iban_banks) if v[0] == iban[4:2]]
    bank_name = dict(_iban_banks)[int(iban[4:6])]
    bank_name_ar = dict(_iban_banks_ar)[int(iban[4:6])]
    return [bank_name, bank_name_ar]


def validate_mobile_number(number):
    if re.match(r'^(009665|9665|\+9665|05)(5|0|3|6|4|9|1|8|7)([0-9]{7})$', number):
        return True
    return False


def convert_greg_to_hijri(day, month, year):
    date = HijriDate(year, month, day, gr=True)
    return date


def convert_hijri_to_greg(day, month, year):
    date = HijriDate(year, month, day)
    return date


def get_today_date():
    date = HijriDate.today()
    return date


def get_hijri_month_length(month, year):
    date = HijriDate(year, month, 1)
    date = HijriDate(int(date.year_gr), int(date.month_gr), int(date.day_gr), gr=True)
    return date.month_len


def validate_id(number):

    number = number.strip()

    if not number.isnumeric() or len(number) != 10:
        return {'valid': False, 'type': '', 'type_ar': '', 'number': number}

    type = number[0]
    if type != '1' and type != '2':
        return {'valid': False, 'type': '', 'type_ar': '', 'number': number}

    summ = 0
    for counter, value in enumerate(number):
        if counter % 2 == 0:
            ZFOdd = str((int(value)*2)).ljust(2, '0')
            summ += int(ZFOdd[0]) + int(ZFOdd[1])
            pass
        else:
            summ += int(value)
    return {'valid': summ % 10 == 0, 'type': dict(_identity_types)[int(type)] if summ % 10 == 0 else '',
            'type_ar': dict(_identity_types_ar)[int(type)].decode('utf-8') if summ % 10 == 0 else '', 'number': number}


def validate_disposable_email(email):
    disposable = False
    domain = email.split("@", 1)[1]
    print domain
    if domain in disposable_emails_list.disposable_emails:
        disposable = True
    return {'email': email, 'disposable': disposable}

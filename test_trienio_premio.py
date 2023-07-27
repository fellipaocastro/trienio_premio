import argparse
from datetime import datetime

import pytest

from trienio_premio import parse_date, calculate_dates, main


def test_parse_valid_date():
    date_str = '01/01/2023'
    result = parse_date(date_str)

    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 1


def test_parse_invalid_date():
    date_str = '2023/01/01'

    with pytest.raises(argparse.ArgumentTypeError, match='Data inválida. Use o formato dd/mm/yyyy.'):
        parse_date(date_str)


def test_calculate_dates():
    start_date = datetime(2021, 1, 19)
    marcos = 11
    anos = 3

    result = calculate_dates(start_date, marcos, anos)

    assert len(result) == marcos
    assert result == [
        '18/01/2024',
        '17/01/2027',
        '16/01/2030',
        '15/01/2033',
        '15/01/2036',
        '14/01/2039',
        '13/01/2042',
        '12/01/2045',
        '12/01/2048',
        '11/01/2051',
        '10/01/2054'
    ]


def test_calculate_dates_zero_intervals():
    start_date = datetime(2023, 1, 1)
    marcos = 0
    anos = 1

    result = calculate_dates(start_date, marcos, anos)

    assert len(result) == 0


def test_main_with_default_dates():
    data_publico = datetime(2021, 1, 19)
    data_rj = datetime(2022, 5, 19)

    result = main(data_publico, data_rj)

    expected_output = [
        (3, ['18/01/2024 | ATS 01 | (10%)']), (5, ['17/05/2027 | Licença-prêmio 01']),
        (6, ['17/01/2027 | ATS 02 | (15%)']), (9, ['16/01/2030 | ATS 03 | (20%)']),
        (10, ['15/05/2032 | Licença-prêmio 02']), (12, ['15/01/2033 | ATS 04 | (25%)']),
        (15, ['15/01/2036 | ATS 05 | (30%)', '14/05/2037 | Licença-prêmio 03']), (18, ['14/01/2039 | ATS 06 | (35%)']),
        (20, ['13/05/2042 | Licença-prêmio 04']), (21, ['13/01/2042 | ATS 07 | (40%)']),
        (24, ['12/01/2045 | ATS 08 | (45%)']), (25, ['12/05/2047 | Licença-prêmio 05']),
        (27, ['12/01/2048 | ATS 09 | (50%)']), (30, ['11/01/2051 | ATS 10 | (55%)', '10/05/2052 | Licença-prêmio 06']),
        (33, ['10/01/2054 | ATS 11 | (60%)']), (35, ['09/05/2057 | Licença-prêmio 07']),
        (40, ['08/05/2062 | Licença-prêmio 08']), (45, ['07/05/2067 | Licença-prêmio 09']),
        (50, ['05/05/2072 | Licença-prêmio 10']), (55, ['04/05/2077 | Licença-prêmio 11'])
    ]

    assert result == expected_output

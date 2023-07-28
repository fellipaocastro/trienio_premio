import argparse
from datetime import datetime

import pytest

from calcula_carreira import parse_date, calculate_dates, main


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
        ('18/01/2024', '3 anos | ATS 01 | (10%)'),
        ('17/01/2027', '6 anos | ATS 02 | (15%)'),
        ('17/05/2027', '5 anos | Licença-prêmio 01'),
        ('16/01/2030', '9 anos | ATS 03 | (20%)'),
        ('15/05/2032', '10 anos | Licença-prêmio 02'),
        ('15/01/2033', '12 anos | ATS 04 | (25%)'),
        ('15/01/2036', '15 anos | ATS 05 | (30%)'),
        ('14/05/2037', '15 anos | Licença-prêmio 03'),
        ('14/01/2039', '18 anos | ATS 06 | (35%)'),
        ('13/01/2042', '21 anos | ATS 07 | (40%)'),
        ('13/05/2042', '20 anos | Licença-prêmio 04'),
        ('12/01/2045', '24 anos | ATS 08 | (45%)'),
        ('12/05/2047', '25 anos | Licença-prêmio 05'),
        ('12/01/2048', '27 anos | ATS 09 | (50%)'),
        ('11/01/2051', '30 anos | ATS 10 | (55%)'),
        ('10/05/2052', '30 anos | Licença-prêmio 06'),
        ('10/01/2054', '33 anos | ATS 11 | (60%)'),
        ('09/05/2057', '35 anos | Licença-prêmio 07'),
        ('08/05/2062', '40 anos | Licença-prêmio 08'),
        ('07/05/2067', '45 anos | Licença-prêmio 09'),
        ('05/05/2072', '50 anos | Licença-prêmio 10'),
        ('04/05/2077', '55 anos | Licença-prêmio 11')
    ]

    assert result == expected_output

import argparse
from datetime import datetime, timedelta


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Data inválida. Use o formato dd/mm/yyyy.') from exc


def calculate_dates(start_date, intervals, interval_years):
    dates = []
    current_date = start_date

    for _ in range(intervals):
        current_date += timedelta(days=365 * interval_years)
        dates.append((current_date - timedelta(days=1)).strftime('%d/%m/%Y'))

    return dates


def main(data_publico, data_rj):
    marcos = 11
    anos_trienio = 3
    anos_premio = 5
    percentual_trienio = 5

    future_ats = calculate_dates(data_publico, marcos, anos_trienio)
    future_license = calculate_dates(data_rj, marcos, anos_premio)

    trienio_premio = {}

    for idx, date in enumerate(future_ats, start=1):
        percentual_trienio += 5

        if anos_trienio not in trienio_premio:
            trienio_premio[anos_trienio] = []

        trienio_premio[anos_trienio].append(f'{date} | ATS {str(idx).zfill(2)} | ({percentual_trienio}%)')

        anos_trienio += 3

    for idx, date in enumerate(future_license, start=1):

        if anos_premio not in trienio_premio:
            trienio_premio[anos_premio] = []

        trienio_premio[anos_premio].append(f'{date} | Licença-prêmio {str(idx).zfill(2)}')

        anos_premio += 5

    return sorted(trienio_premio.items())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calcula ATS e licença-prêmio.')
    parser.add_argument('--data_publico', type=parse_date, default='19/01/2021',
                        help='Ingresso no serviço público no formato dd/mm/yyyy (opcional, padrão: 19/01/2021).')
    parser.add_argument('--data_rj', type=parse_date, default='19/05/2022',
                        help='Ingresso no Estado do RJ no formato dd/mm/yyyy (opcional, padrão: 19/05/2022).')
    args = parser.parse_args()

    calculos = main(args.data_publico, args.data_rj)

    for anos, valores in calculos:
        for valor in valores:
            print(f'{str(anos).zfill(2)} anos: {valor}')

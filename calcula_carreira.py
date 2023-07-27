import argparse
from datetime import datetime, timedelta
from colorama import init, Fore

init(autoreset=True)


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Data inválida. Use o formato dd/mm/yyyy.') from exc


def calculate_dates(start_date, intervals, interval_years):
    dates = []
    date = start_date

    for _ in range(intervals):
        date += timedelta(days=365 * interval_years)
        dates.append((date - timedelta(days=1)).strftime('%d/%m/%Y'))

    return dates


def main(data_publico, data_rj, datas_tce):
    marcos = 11
    anos_trienio = 3
    anos_premio = 5
    anos_progressao = 3
    percentual_trienio = 5
    percentual_progressao = 5

    future_ats = calculate_dates(data_publico, marcos, anos_trienio)
    future_license = calculate_dates(data_rj, marcos, anos_premio)
    future_progress = calculate_dates(data_tce, marcos, anos_progressao)

    trienio_premio = []

    for idx, date in enumerate(future_ats, start=1):
        percentual_trienio += 5
        trienio_premio.append((date, f'{anos_trienio} anos | ATS {str(idx).zfill(2)} | ({percentual_trienio}%)'))
        anos_trienio += 3

    for idx, date in enumerate(future_license, start=1):
        trienio_premio.append((date, f'{anos_premio} anos | Licença-prêmio {str(idx).zfill(2)}'))
        anos_premio += 5

    for idx, date in enumerate(future_progress, start=1):
        percentual_progressao += 5
        trienio_premio.append((date, f'{anos_progressao} anos | ATS {str(idx).zfill(2)} | ({percentual_progressao}%)'))
        anos_progressao += 3

    trienio_premio.sort(key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))

    return trienio_premio


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calcula ATS e licença-prêmio.')
    parser.add_argument('--ingresso_publico', type=parse_date, default='19/01/2021',
                        help='Ingresso no serviço público no formato dd/mm/yyyy (opcional, padrão: 19/01/2021).')
    parser.add_argument('--ingresso_rj', type=parse_date, default='19/05/2022',
                        help='Ingresso no Estado do RJ no formato dd/mm/yyyy (opcional, padrão: 19/05/2022).')
    parser.add_argument('--ingresso_tce', type=parse_date, default='22/03/2023',
                        help='Ingresso no TCE-RJ no formato dd/mm/yyyy (opcional, padrão: 22/03/2023).')
    args = parser.parse_args()

    current_date = datetime.now()
    calculos = main(args.data_publico, args.data_rj, args.data_tce)

    FIRST_HIGHLIGHTED = False

    for data, valor in calculos:
        if not FIRST_HIGHLIGHTED and datetime.strptime(data, '%d/%m/%Y') >= current_date:
            print(f'{Fore.RED}{data}: {valor}')
            FIRST_HIGHLIGHTED = True
        else:
            print(f'{data}: {valor}')

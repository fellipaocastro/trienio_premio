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


def main(ingresso_publico, ingresso_rj, ingresso_tce):
    marcos = 11
    anos_trienio = 3
    anos_premio = 5
    anos_progressao = 3
    percentual_trienio = 5
    percentual_progressao = 5

    calculos = []

    highlighted_ingresso_publico = False
    highlighted_ingresso_rj = False
    highlighted_ingresso_tce = False


    current_date = datetime.now()

    if ingresso_publico:
        future_ats = calculate_dates(ingresso_publico, marcos, anos_trienio)

        for idx, date in enumerate(future_ats, start=1):
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            percentual_trienio += 5
            cor = ''

            if date_obj >= current_date and not highlighted_ingresso_publico:
                cor = Fore.RED
                highlighted_ingresso_publico = True

            calculos.append((date, f'{cor}{anos_trienio} anos | ATS {str(idx).zfill(2)} | ({percentual_trienio}%)'))
            anos_trienio += 3

    if ingresso_rj:
        future_license = calculate_dates(ingresso_rj, marcos, anos_premio)

        for idx, date in enumerate(future_license, start=1):
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            cor = ''

            if date_obj >= current_date and not highlighted_ingresso_rj:
                cor = Fore.YELLOW
                highlighted_ingresso_rj = True

            calculos.append((date, f'{cor}{anos_premio} anos | Licença-prêmio {str(idx).zfill(2)}'))
            anos_premio += 5

    if ingresso_tce:
        future_progress = calculate_dates(ingresso_tce, marcos, anos_progressao)

        for idx, date in enumerate(future_progress, start=1):
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            percentual_progressao += 5
            cor = ''

            if date_obj >= current_date and not highlighted_ingresso_tce:
                cor = Fore.BLUE
                highlighted_ingresso_tce = True

            calculos.append((date, f'{cor}{anos_progressao} anos | ATS {str(idx).zfill(2)} | ({percentual_progressao}%)'))
            anos_progressao += 3

    calculos.sort(key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))

    return calculos


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calcula ATS e licença-prêmio.')
    parser.add_argument('--ingresso_publico', type=parse_date,
                        help='Ingresso no serviço público no formato dd/mm/yyyy.')
    parser.add_argument('--ingresso_rj', type=parse_date,
                        help='Ingresso no Estado do RJ no formato dd/mm/yyyy.')
    parser.add_argument('--ingresso_tce', type=parse_date,
                        help='Ingresso no TCE-RJ no formato dd/mm/yyyy.')
    args = parser.parse_args()

    calculos = main(args.ingresso_publico, args.ingresso_rj, args.ingresso_tce)

    for data, valor in calculos:
        print(f'{data}: {valor}')

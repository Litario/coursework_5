from datetime import datetime

from sup.constants import NONCOLOR, YELLOW, GREEN


def color_print(date: list) -> None:
    """Печатает цветные словари из списка"""

    if isinstance(date, list):
        for i in date:
            if isinstance(i, tuple) and len(i) == 2:
                i_dict = dict([i])
                for k, v in i_dict.items():
                    print(f'{k} : {GREEN} {v} {NONCOLOR}')

            elif isinstance(i, dict):
                for k, v in i.items():
                    print(f'{k} : {GREEN} {v} {NONCOLOR}')
                print()
            else:
                print('Доработать функцию.')

    elif isinstance(date, dict):
        for k, v in date.items():
            print(f'{k} : {GREEN} {v} {NONCOLOR}')
        print()

    else:
        print('Доработать функцию.')


def write_datetime(file_name: str, format: str) -> None:
    """Записывает время создания БД в указанный файл."""

    with open(file_name, mode='w') as file:
        now = datetime.now()
        db_create_datetime = datetime.strftime(now, format)
        file.write(db_create_datetime)

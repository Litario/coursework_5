from sup.constants import NONCOLOR, YELLOW, GREEN


def colprint(date: list) -> None:
    """Печать словарей из списка"""

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

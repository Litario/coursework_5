import json
from pprint import pprint
from icecream import ic
from datetime import datetime

import requests

from sup.adress import WORK_JSON_PATH


def get_employers_data(firms: list[str], per_page: int = 10) -> list[dict]:
    vac_url = 'https://api.hh.ru/vacancies'

    data = []
    for employer_id in firms:
        params = {'employer_id': employer_id, 'per_page': per_page}

        try:
            response: dict = requests.get(url=vac_url, params=params).json()
            vacancies: list = response['items']
            data.append(
                {'employer_HHid': employer_id,
                 'employer': vacancies[0]['employer']['name'],
                 'vacancies': vacancies,
                 'vacancies_number': response['found']
                 }
            )
        except Exception:
            continue

    # return response
    return data


firms = ['169209',  # ГУД ВУД
         '64174',  # 2ГИС
         '3344',  # ЛСР
         '12550',  # ПИК
         '1102601',  # Самолет
         '2180488',  # ЭТАЛОН
         '68268',  # Пионер
         '1066018',  # Брусника
         ]

dt = get_employers_data(firms)

# pprint(dt,
#        indent=1,
#        stream=print(),
#        depth=None,
#        compact=False,
#        sort_dicts=False
#        )

with open(WORK_JSON_PATH, mode='w', encoding='utf-8') as file:
    json.dump(dt, file, ensure_ascii=False, indent=4)


# for i in dt:
#     print(i['vacancies'][0]['employer']['name'])

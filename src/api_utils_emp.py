import json
from pprint import pprint
from icecream import ic
from datetime import datetime

import requests

from sup.adress import WORK_JSON_PATH


def get_employers_data(firms, per_page: int = 100):
    vac_url = 'https://api.hh.ru/employers'

    params = {'name': 'ГУД ВУД', 'per_page': per_page}

    response = requests.get(url=vac_url, params=params).json()
        # vacancies: list = response['items'][3]

        # data.append(
        #     {'employer': firm,
        #      'vacancies': vacancies,
        #      'vacancies_number': response['found']
        #      }
        # )

    return response
    # return data


firms = ['169209']
dt = get_employers_data(firms)
# print(len(dt[0]['data']))

pprint(dt,
       indent=1,
       stream=print(),
       depth=None,
       compact=False,
       sort_dicts=True
       )

# with open(WORK_JSON_PATH, mode='w', encoding='utf-8') as file:
#     json.dump(dt, file, ensure_ascii=False, indent=4)


# for i in dt:
#     print(i['vacancies'][0]['employer']['name'])

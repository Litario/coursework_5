import requests


def get_employers_data(firms: list[str], per_page: int = 12) -> list[dict]:
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

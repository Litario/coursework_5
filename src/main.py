from conf.config import config
from src.api_utils import get_employers_data
from src.database_utils import create_database, save_data_to_database


def main():

    create_database_task = input("\nПриветствую.\n"
                          "Это скрипт для создания базы данных (БД) в postgresql\n"
                          "вакансий работодателей с сайта HeadHunter и последующей работы с этой БД.\n"
                          "Список с id работодателей (id нужно взять с сайта HeadHunter "
                          "\n"
                          "Хотите создать (обновить) БД \n"
                          "[Нажмите Enter, чтобы пропустить вопрос]")

    if create_database_task in ('да', 'yes'):
        ## обновление базы данных с курсами валют относительно рубля
        get_currency_rate()







    firms = ['169209',  # ГУД ВУД
             '64174',  # 2ГИС
             '3344',  # ЛСР
             '12550',  # ПИК
             '1102601',  # Самолет
             '2180488',  # ЭТАЛОН
             '68268',  # Пионер
             '1066018',  # Брусника
             ]

    # data = get_employers_data(firms)
    #
    # params = config()
    # # print(params)
    # data_base_name = 'headhunter'
    # create_database(data_base_name, params)
    # save_data_to_database(data, data_base_name, params)


if __name__ == '__main__':
    main()

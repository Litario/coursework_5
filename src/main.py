from common_functions.funcs import color_print, write_datetime
from conf.config import config
from src.classes import DBManager
from src.utils_api import get_employers_data
from src.utils_database import create_database, save_data_to_database
from sup.constants import NONCOLOR, YELLOW, BLUE, RED, GREEN
from ts.firms import firms, firms_last_dir


def main():
    with open('datetime.txt', mode='r') as file:
        db_create_datetime = file.read()

    print("\nПриветствую.\n"
          "\n"
          f"Это скрипт для создания в {BLUE}postgresql{NONCOLOR} базы данных (БД)\n"
          f"вакансий работодателей с сайта {BLUE}HeadHunter{NONCOLOR} и последующей работы с этой БД.\n"
          f"Список с id работодателей (id с сайта HeadHunter) нужно заполнить в файле {YELLOW}<{firms_last_dir}>{NONCOLOR}.\n")

    data_base_name = 'headhunter'
    params = config()

    if not db_create_datetime:
        create_db_task = input("БД создается впервые.\n"
                               "Хотите продолжить (да / yes) ?\n"
                               "[Нажмите Enter, чтобы отказаться]\n")

        if create_db_task in ('да', 'yes'):
            ## создание базы данных
            data = get_employers_data(firms)
            create_database(data_base_name, params)
            save_data_to_database(data, data_base_name, params)

            write_datetime('datetime.txt', '%Y-%m-%d %H:%M')

            flag = True

    else:
        work_db_task = input(f"Последняя БД была создана в {BLUE}{db_create_datetime}{NONCOLOR}.\n"
                             f"{YELLOW}Варианты действий:{NONCOLOR}\n"
                             "1 - обновить БД и продолжить работу с ней\n"
                             "2 - продолжить работать с существующей БД\n"
                             "3 - закончить работу\n")

        if work_db_task not in ('1', '2'):
            flag = False

        elif work_db_task == '1':
            ## обновление базы данных
            data = get_employers_data(firms)
            create_database(data_base_name, params)
            save_data_to_database(data, data_base_name, params)

            write_datetime('datetime.txt', '%Y-%m-%d %H:%M')

            flag = True

        elif work_db_task == '2':
            flag = True

    while flag:
        counter = 0
        max_counter = 7  # количество ложных обращений к БД, запрошенных подряд

        while counter < max_counter:
            db = DBManager(data_base_name)

            db_task = input(f"\n{YELLOW}Возможные действия с БД:{NONCOLOR}\n"
                            "0 - завершить работу\n"
                            "1 - вывести список всех компаний и количество вакансий у каждой компании\n"
                            "2 - вывести список всех вакансий с указанием названия компании, названия вакансии,\n"
                            "    нижнего порога зарплаты и ссылки на вакансию\n"
                            "3 - вывести среднюю зарплату по вакансиям\n"
                            "4 - вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                            "5 - вывести список всех вакансий, в названии которых содержатся\n"
                            "    переданные в метод слова, (например слово <менеджер>)\n")

            if db_task == '0':
                flag = False
                break

            elif db_task == '1':
                counter = 0
                color_print(db.get_companies_and_vacancies_count())

            elif db_task == '2':
                counter = 0
                print(*[f"{BLUE}{i[0]}{NONCOLOR} \n {i[1:]}" for i in db.get_all_vacancies()],
                      sep='\n')

            elif db_task == '3':
                counter = 0
                for tpl in db.get_avg_salary():
                    print(f"компания: {BLUE}{tpl[0]}{NONCOLOR}\n"
                          f"вакансия: {GREEN}{tpl[1]}{NONCOLOR}\n"
                          f"средняя ЗП: {GREEN}{str(tpl[2]) + ' ' + tpl[3]}{NONCOLOR}\n")

                # print(*[f"{BLUE}{i[0]}{NONCOLOR} \n {i[1:]}" for i in db.get_avg_salary()],
                #       sep='\n')


            elif db_task == '4':
                counter = 0
                for tpl in db.get_vacancies_with_higher_salary():
                    print(f"компания: {BLUE}{tpl[0]}{NONCOLOR}\n"
                          f"вакансия: {GREEN}{tpl[1]}{NONCOLOR}\n"
                          f"ЗП: {GREEN}{str(tpl[2]) + ' ' + tpl[3]}{NONCOLOR}\n")


            elif db_task == '5':
                counter = 0
                keyword = input(f"{YELLOW}Введите поисковое слово{NONCOLOR}\n")
                color_print(db.get_vacancies_with_keyword(key_word=keyword))

            else:
                print(f"{RED}Нет такого действия, повторите попытку.{NONCOLOR}\n")
                counter += 1

        else:
            print("Все, ты надоел.")
            break


if __name__ == '__main__':
    main()

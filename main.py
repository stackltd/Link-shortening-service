import pprint

from storage import *
from regex import *
from url_request import check_page
from messages import *


def main():
    print('Программа для сокращения интернет-адресов')
    while True:
        ask = input(main_menu)
        if ask == '1':
            try:
                url = input('Введите стандартный url для регистрации:\n')
                short_name = shorts_json_maker(url_in=url)
                pseudoname = pseudo_home_page(url=url)
                print('Короткий интернет-адрес:', short_name)
                print('Псевдоним домашней страницы:', pseudoname)
                print('Стандартный интернет-адрес:', url)
            except IndexError:
                print('Ошибка! Введите корректный адрес')
                # raise
        elif ask == '2':
            pseudo = input('Введите псевдоним домашней страницы: ')
            home_pages_from_pseudo(pseudo=pseudo)
        elif ask == '3':
            short = input('Введите сокращенный url: ')
            source_url = url_from_token(short=short)
            if source_url:
                print('Стандартный интернет-адрес:', source_url)
                print('Короткий интернет-адрес:', short)
                code_response = check_page(url=source_url)
                print('Код ответа:', code_response)
        elif ask == '4':
            print('Псевдонимы:')
            with open('dumps/pseudonames.json', 'r', encoding='utf-8') as file:
                pseudo_names: dict = json.load(file)
                pprint.pprint(pseudo_names)
            print('\n\nКороткие интернет-адреса:')
            with open('dumps/shorts.json', 'r', encoding='utf-8') as file:
                shorts: dict = json.load(file)
                pprint.pprint(shorts)
        elif ask == '5':
            print('Программа завершена')
            break
        else:
            print('Ошибка. Выберите требуемый пункт меню')


if __name__ == '__main__':
    main()

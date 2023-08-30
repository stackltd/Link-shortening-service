import random
import json

import pprint

from regex import short_address, pseudo_home_page, home_page
from url_request import check_page

ALPH = 'abcdefghijklmnopqrstuvwxyz'


def __token_gen() -> str:
    """
    Функция генерирует токен из 4 символов латинского алфавита
    """
    return ''.join([random.choice(ALPH) for _ in range(4)])


def shorts_json_maker(url_in: str) -> str:
    """
    Функция пополняет базу данных коротких ссылок, соответствующих переданному url и возвращает ссылку
    :param url_in: входящий url адрес
    :return: короткая ссылка
    """
    with open('dumps/shorts.json', 'r', encoding='utf-8') as file:
        shorts: dict = json.load(file)
    keys = list(shorts.keys())
    values = list(shorts.values())
    if keys:
        if url_in in values:
            index = values.index(url_in)
            short_name = keys[index]
            print('Данный url уже зарегистрирован')
        else:
            while True:
                token = __token_gen()
                short_name = short_address(url=url_in, token=token)
                # проверяем, что сгенерированного токена нет в базе
                if short_name not in keys:
                    shorts.update({short_name: url_in})
                    with open(f'dumps/shorts.json', 'w', encoding='utf-8') as file:
                        json.dump(shorts, file, indent=4, ensure_ascii=False)
                    break
    else:
        token = __token_gen()
        short_name = short_address(url=url_in, token=token)
        shorts.update({short_name: url_in})
        with open(f'dumps/shorts.json', 'w', encoding='utf-8') as file:
            json.dump(shorts, file, indent=4, ensure_ascii=False)
        # пополняем базу данных домашних страниц
    __pseudo_to_home_pages_json_maker(url_in)
    return short_name


def url_from_token(short):
    """"""
    # Функция возвращает исходный url по токену
    with open('dumps/shorts.json', 'r', encoding='utf-8') as file:
        shorts: dict = json.load(file)
    keys = shorts.keys()
    if short in keys:
        url = shorts[short]
        return url
    else:
        print('Стандартный интернет-адрес не найден')


def __pseudo_to_home_pages_json_maker(url: str) -> None:
    """
    Функция формирует базу данных всех возможных домашних страниц, соответствующих какому-либо псевдониму,
    полученному из url.
    """
    home_page_url = home_page(url)
    pseudo = pseudo_home_page(url)
    with open('dumps/pseudonames.json', 'r', encoding='utf-8') as file:
        pseudo_names: dict = json.load(file)
    value = pseudo_names.get(pseudo)
    if value is not None:
        if home_page_url not in value:
            pseudo_names[pseudo].append(home_page_url)
            with open(f'dumps/pseudonames.json', 'w', encoding='utf-8') as file:
                json.dump(pseudo_names, file, indent=4, ensure_ascii=False)
    else:
        pseudo_names.update({pseudo: [home_page_url]})
        with open(f'dumps/pseudonames.json', 'w', encoding='utf-8') as file:
            json.dump(pseudo_names, file, indent=4, ensure_ascii=False)


def home_pages_from_pseudo(pseudo: str) -> None:
    """
    Функция получает на вход псевдоним домашней страницы и проверяет все соответствующие ему домашние страницы,
     отправляя им get-зппрос
    :param pseudo:
    :return:
    """
    with open('dumps/pseudonames.json', 'r', encoding='utf-8') as file:
        pseudo_names: dict = json.load(file)
        if pseudo in pseudo_names.keys():
            urls_list = pseudo_names[pseudo]
            nubmer_address = len(urls_list)
            print('Найдено адресов:', nubmer_address)
            for index, url in enumerate(urls_list):
                if nubmer_address > 1:
                    print(f'Адрес {index + 1}:')
                print('Стандартный интернет-адрес: ', url)
                print('Псевдоним домашней страницы интернет-адреса:', pseudo)
                code_response = check_page(url)
                print('Код ответа:', code_response)
        else:
            print('Адрес домашней страницы не найден')


def print_database():
    print('Псевдонимы:')
    with open('dumps/pseudonames.json', 'r', encoding='utf-8') as file:
        pseudo_names: dict = json.load(file)
        if pseudo_names:
            pprint.pprint(pseudo_names)
        else:
            print('Нет данных')
    print('\nКороткие интернет-адреса:')
    with open('dumps/shorts.json', 'r', encoding='utf-8') as file:
        shorts: dict = json.load(file)
        if shorts:
            pprint.pprint(shorts)
        else:
            print('Нет данных')

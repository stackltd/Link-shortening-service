import random
import json

from regex import *
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
            ind = values.index(url_in)
            short_name = keys[ind]
            print('Данный url уже зарегистрирован')
        else:
            while True:
                token = __token_gen()
                # проверяем, что сгенерированного токена нет в базе
                if token not in keys:
                    short_name = short_address(url=url_in, token=token)
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
            nubm_address = len(urls_list)
            print('Найдено адресов:', nubm_address)
            for ind, url in enumerate(urls_list):
                if nubm_address > 1:
                    print(f'Адрес {ind + 1}:')
                print('Стандартный интернет-адрес: ', url)
                print('Псевдоним домашней страницы интернет-адреса:', pseudo)
                code_response = check_page(url)
                print('Код ответа:', code_response)
        else:
            print('Адрес домашней страницы не найден')

import requests
from requests.exceptions import ConnectionError


def check_page(url):
    """
    Функция возвращает код ответа сервера на get-запрос
    """
    try:
        result = requests.get(url)
        code_response = result.status_code
        return code_response
    except ConnectionError:
        return '404 (NOT_FOUND)'
        # raise

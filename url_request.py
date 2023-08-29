import requests


def check_page(url):
    """
    Функция возвращает код ответа сервера на get-запрос
    """
    try:
        res = requests.get(url)
        code_response = res.status_code
        return code_response
    except Exception:
        return '404 (NOT_FOUND)'
        # raise


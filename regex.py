import re

PATTERNS = [r'[a-z0-9-]+\.?[a-z0-9-]+\.[a-z]{2,}',
            r'w{3}\.',
            r'[a-z]+\.([a-z0-9-]+)\.[a-z]+',
            r'[a-z0-9-]+\.',
            r'.+\.[a-z]{2,}']


def pseudo_home_page(url: str) -> str:
    """
    Функция формирует псевдоним домашней страницы
    """
    # удаляем символы 'https://'
    result1 = re.findall(PATTERNS[0], url)[0]
    # удаляем символы 'www.'
    result2 = re.sub(PATTERNS[1], '', result1)
    # получаем домашнюю страницу, если страница имеет вид типа 'go.skilbox.ru'
    result_corrected = re.findall(PATTERNS[2], result2)
    if result_corrected:
        result = result_corrected[0]
    else:
        # получаем домашнюю страницу, если страница имеет вид типа 'online.ru'
        result_corrected = re.findall(PATTERNS[3], result2)
        result = result_corrected[0][:-1]
    return result


def short_address(url: str, token: str) -> str:
    """
    Функция формирует короткий адрес из псевдонима и токена
    """
    # получаем псевдоним
    pseudo = pseudo_home_page(url)
    # формируем новый домен для короткого адреса
    if len(pseudo) >= 5:
        result = pseudo[:5]
        result = ''.join([result[:3], '.', result[3:]])
    else:
        result = ''.join([pseudo, '.', pseudo])
    return '/'.join([result, token])


def home_page(url: str) -> str:
    """
    Функция выделяет домашнюю страницу из url
    """
    result = re.findall(PATTERNS[4], url)[0]
    return result

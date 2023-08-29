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
    res1 = re.findall(PATTERNS[0], url)[0]
    # удаляем символы 'www.'
    res2 = re.sub(PATTERNS[1], '', res1)
    # получаем домашнюю страницу, если страница имеет вид типа 'go.skilbox.ru'
    res_corr = re.findall(PATTERNS[2], res2)
    if res_corr:
        res = res_corr[0]
    else:
        # получаем домашнюю страницу, если страница имеет вид типа 'online.ru'
        res_corr = re.findall(PATTERNS[3], res2)
        res = res_corr[0][:-1]
    return res


def short_address(url: str, token: str) -> str:
    """
    Функция формирует короткий адрес из псевдонима и токена
    """
    # получаем псевдоним
    pseudo = pseudo_home_page(url)
    # формируем новый домен для короткого адреса
    if len(pseudo) >= 5:
        res = pseudo[:5]
        res = ''.join([res[:3], '.', res[3:]])
    else:
        res = ''.join([pseudo, '.', pseudo])
    return '/'.join([res, token])


def home_page(url: str) -> str:
    """
    Функция выделяет домашнюю страницу из url
    """
    res = re.findall(PATTERNS[4], url)[0]
    return res

def check_url(url: str) -> bool:
    return url.startswith('https://') | url.startswith('http://')


if __name__ == '__main__':
    print(check_url('http:/yandex.ru'))

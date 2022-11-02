from allure import step

from core.helpers import check_url
from elements.elements import Elements


class GooglePage(Elements):
    def __init__(self, browser, base_url: str):
        self.driver = browser
        self.base_url = base_url

    @step('Открытие страницы')
    def open(self, url='/'):
        self.driver.open(url if check_url(url=url) else f'{self.base_url}{url}')

    @step('Заполнения поля поиска значением {value}')
    def fill_search_form(self, value):
        self.element('[title="Поиск"]').set_value(value)

    @step('Клик по кнопке поиска')
    def click_button(self):
        self.element('[title="Поиск"]').press_enter()

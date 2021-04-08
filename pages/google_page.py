from allure import step

from components.elements import Elements


class GooglePage(Elements):
    def __init__(self, browser):
        self.driver = browser

    @step('Открытие страницы')
    def open(self, url='/'):
        self.driver.open(url)

    @step('Заполнения поля поиска значением {value}')
    def fill_search_form(self, value):
        self.input('[title="Поиск"]').set_value(value)

    @step('Клик по кнопке поиска')
    def click_button(self):
        self.button('[value="Поиск в Google"]').click()

from allure import title, description, suite

from constants.application import PROGNOZ_TEST


@title('Скрин редактирования')
@description('Проверка редактирования')
@suite('Проверка редактирования')
def test_application_login(edit_page, close_application):
    edit_page.user_login(PROGNOZ_TEST)
    edit_page.edit_form('Test')
    edit_page.click_btn()

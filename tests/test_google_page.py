from allure import title, description, suite


@title('Проверка страницы поиска Google')
@description('Проверка страницы поиска Google')
@suite('Проверка страницы поиска Google')
def test_google_search(google_page):
    google_page.open()
    google_page.fill_search_form('Тест')
    google_page.click_button()

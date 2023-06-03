from core.allure_wrapper import step

from selene import by, be, Browser


class GooglePage:
    def __init__(self, browser: Browser, base_url: str):
        self.driver = browser
        self.base_url = base_url
        self.el = self.driver.element

    @step('Opening a page')
    def open(self, url='/'):
        self.driver.open(f"{self.base_url}{url}")

    @step('Filling in the search field with the value {value}')
    def fill_search_form(self, value):
        self.el(by.xpath('//*[@type="search"]')).set_value(value)

    @step('Click on the search button')
    def click_button(self):
        self.el(by.xpath('//*[@type="search"]')).press_enter()

    @step('Checking the visibility of the number of results')
    def should_be_visible_results_search(self):
        self.el(by.id("result-stats")).should(be.visible)

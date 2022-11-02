import pytest
from pages.google_page import GooglePage


@pytest.fixture(scope='function')
def google_page(browser, base_url):
    return GooglePage(browser=browser, base_url=base_url)

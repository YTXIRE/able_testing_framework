import pytest

from config import settings_config
from pages.google_page import GooglePage


@pytest.fixture(scope='function')
def google_page(browser):
    return GooglePage(browser=browser, base_url=settings_config.application_url)

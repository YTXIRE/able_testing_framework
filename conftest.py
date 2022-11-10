from os import getenv

import pytest
from selenium import webdriver
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from core.helpers import get_settings, get_fixtures, get_current_folder
from selene import browser as driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.ie.service import Service
from selene.managed import config

mode = 'local'
settings_config = {}
pytest_plugins = get_fixtures()


def pytest_sessionstart():
    global settings_config
    disable_warnings(InsecureRequestWarning)
    settings_config = get_settings(environment=getenv('environment'))


def pytest_addoption(parser):
    parser.addoption('--mode', action='store', default='local')
    parser.addoption('--browser', action='store', default='chrome')


def _create_driver_with_browser_name(*, browser_name='chrome', options):
    match browser_name:
        case 'firefox':
            config.driver = webdriver.Firefox(
                serive=Service(GeckoDriverManager().install()),
                options=options
            )
        case 'ie':
            config.driver = webdriver.Ie(
                serive=Service(IEDriverManager().install()),
                options=options
            )
        case _:
            config.driver = webdriver.Chrome(
                serive=Service(ChromeDriverManager().install()),
                options=options
            )


@pytest.fixture(scope='function')
def browser(pytestconfig):
    global mode
    mode = pytestconfig.getoption('mode')
    browser_name = pytestconfig.getoption('browser')
    match browser_name:
        case 'firefox':
            options = webdriver.FirefoxOptions()
            options.set_preference('browser.download.dir', get_current_folder(folder='files'))
        case 'ie':
            options = webdriver.IeOptions()
        case _:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.notifications': 1,
                'download.default_directory': get_current_folder(folder='files')
            })
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--allow-running-insecure-content')
    settings_config['BROWSER_NAME'] = browser_name if browser_name != 'chrome' else settings_config['BROWSER_NAME']
    match mode:
        case 'selenoid':
            capabilities = {
                'browserName': settings_config['BROWSER_NAME'],
                'browserVersion': settings_config['SELENOID']['BROWSER_VERSION'],
                'selenoid:options': {
                    'enableVNC': settings_config['SELENOID']['ENABLE_VNC'],
                    'enableVideo': settings_config['SELENOID']['ENABLE_VIDEO']
                }
            }
            config.driver = webdriver.Remote(
                command_executor=settings_config['SELENOID']['HUB'],
                desired_capabilities=capabilities,
                options=options
            )
        case 'headless':
            options.add_argument('--headless')
            _create_driver_with_browser_name(browser_name=browser_name, options=options)
        case _:
            _create_driver_with_browser_name(browser_name=browser_name, options=options)
    config.browser_name = settings_config['BROWSER_NAME']
    config.window_width = settings_config['BROWSER_WINDOW_WIDTH']
    config.window_height = settings_config['BROWSER_WINDOW_HEIGHT']
    config.timeout = settings_config['TIMEOUT']
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def base_url():
    return settings_config['APPLICATION_URL']

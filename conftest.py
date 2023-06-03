from pathlib import Path
from typing import Any

import pytest
from selene import Browser, Config
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Remote
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config import settings_config
from core.helpers import get_fixtures

pytest_plugins = get_fixtures()


def pytest_sessionstart() -> None:
    """Отключение уведомлений."""
    disable_warnings(InsecureRequestWarning)


def pytest_addoption(parser: Any) -> None:
    """Чтение переданных конфигов."""
    parser.addoption("--mode", action="store", default="local")
    parser.addoption("--browser", action="store", default="chrome")


def _create_driver_with_browser_name(
    options: Any,
    browser_name: str = "chrome",
) -> Browser:
    """Создание экземпляра браузера."""
    match browser_name:
        case "firefox":
            return Browser(
                Config(
                    driver=Firefox(
                        executable_path=GeckoDriverManager().install(),
                        options=options,
                    ),
                    base_url=settings_config.application_url,
                    timeout=settings_config.timeout,
                    driver_name=settings_config.browser_name,
                    window_width=settings_config.browser_window_width,
                    window_height=settings_config.browser_window_height,
                )
            )
        case _:
            return Browser(
                Config(
                    driver=Chrome(
                        executable_path=ChromeDriverManager().install(),
                        options=options,
                    ),
                    base_url=settings_config.application_url,
                    timeout=settings_config.timeout,
                    driver_name=settings_config.browser_name,
                    window_width=settings_config.browser_window_width,
                    window_height=settings_config.browser_window_height,
                )
            )


@pytest.fixture(scope="function")
def browser(pytestconfig: Any) -> Any:
    mode = pytestconfig.getoption("mode")
    browser_name = pytestconfig.getoption("browser")
    match browser_name:
        case "firefox":
            options = FirefoxOptions()
            options.set_preference(
                "browser.download.dir",
                str(Path("files").resolve()),
            )
        case _:
            options = ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option(
                "prefs",
                {
                    "profile.default_content_setting_values.notifications": 1,
                    "download.default_directory": str(Path("files").resolve()),
                },
            )
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--privileged")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    settings_config.browser_name = (
        settings_config.browser_name if browser_name == "chrome" else browser_name
    )
    match mode:
        case "selenoid":
            capabilities = {
                "browserName": settings_config.browser_name,
                "browserVersion": settings_config.selenoid.browser_version,
                "selenoid:options": {
                    "enableVNC": settings_config.selenoid.enable_vnc,
                    "enableVideo": settings_config.selenoid.enable_vnc,
                },
            }
            driver = Browser(
                Config(
                    driver=Remote(
                        command_executor=settings_config.selenoid.hub,
                        desired_capabilities=capabilities,
                        options=options,
                    ),
                    base_url=settings_config.application_url,
                    timeout=settings_config.timeout,
                    driver_name=settings_config.browser_name,
                    window_width=settings_config.browser_window_width,
                    window_height=settings_config.browser_window_height,
                )
            )
        case "headless":
            options.add_argument("--headless")
            driver = _create_driver_with_browser_name(browser_name=browser_name, options=options)
        case _:
            driver = _create_driver_with_browser_name(browser_name=browser_name, options=options)
    yield driver
    driver.quit()

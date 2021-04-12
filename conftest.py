from os import environ, getenv

import pytest
from selene.support.shared import config, browser as driver
from pywinauto import Application

from core.helpers import get_settings

from pages.google_page import GooglePage
from pages.edit_page import EditPage

from models.language import Language


@pytest.fixture(scope='module')
def browser(get_environment):
    config.browser_name = 'chrome'
    config.base_url = get_settings(environment=get_environment)['APPLICATION_URL']
    return driver


@pytest.fixture(scope='module')
def get_environment():
    if getenv('environment') is None:
        environ['environment'] = 'test'
    return getenv('environment')


@pytest.fixture(scope='function')
def google_page(browser):
    return GooglePage(browser)


@pytest.fixture(scope='function')
def application(get_environment):
    return Application(backend=get_settings(environment=get_environment)['APPLICATION_TYPE'])\
        .start(get_settings(environment=get_environment)['APPLICATION_PATH'])


@pytest.fixture(scope='function')
def window_app(application):
    return application.window(title=get_settings(environment=get_environment)['APPLICATION_TITLE'])


@pytest.fixture(scope='function')
def edit_page(window_app):
    return EditPage(window_app)


@pytest.fixture(scope='function')
def close_application(window_app):
    yield window_app.close()


@pytest.fixture(scope='function')
def get_langs_ids(get_environment):
    lang = Language()
    ids_list = []
    for lang in lang.get_lang(environment=get_environment):
        ids_list.append(lang.id)
    return ids_list


@pytest.fixture(scope='function')
def add_lang(get_environment):
    new_lang = Language(
        name='Ru',
        iso_code='ru',
        code='Ru',
        voice_name='Ru'
    )
    new_lang.add_lang(environment=get_environment, query=new_lang)


@pytest.fixture(scope='function')
def add_langs(get_environment):
    langs = []
    lang = Language()
    for item in range(1, 10):
        langs.append(
            Language(
                name=item,
                iso_code=item,
                code=item,
                voice_name=item
            )
        )
    lang.add_langs(environment=get_environment, query=langs)


@pytest.fixture(scope='function')
def update_lang(get_environment):
    lang = Language()
    return lang.update_lang(environment=get_environment, condition={'id': 104}, update_value={'name': 'qwerty'})


@pytest.fixture(scope='function')
def delete_lang(get_environment):
    lang = Language()
    lang.delete_lang(environment=get_environment, condition={'id': 104})


@pytest.fixture(scope='function')
def execute_lang(get_environment):
    lang = Language()
    return lang.execute_lang(environment=get_environment, query='SELECT * FROM languages')


@pytest.fixture(scope='function')
def get_lang_by_id(get_environment):
    lang = Language()
    print(lang.get_lang_by(environment=get_environment, condition={'name': '1'}))
    return 1

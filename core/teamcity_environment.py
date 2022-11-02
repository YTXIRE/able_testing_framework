from os import getenv
from configparser import ConfigParser

from core.helpers import get_file_path


def set_testrun_name_from_teamcity(*, path: str):
    parser = ConfigParser()
    parser.read(path)
    parser.get('testit', 'testrun_name')
    parser.set("testit", "testrun_name", getenv("testrun_name"))
    with open(path, 'w') as testrun_name_testit:
        parser.write(testrun_name_testit)


if __name__ == "__main__":
    set_testrun_name_from_teamcity(path=get_file_path(filename="connection_config.ini"))

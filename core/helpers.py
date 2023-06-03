import json
from os import getcwd, walk
from os.path import join
from pathlib import Path


def get_current_folder(folder: str) -> str:
    current = getcwd()

    def find_folder(path: str or Path) -> str:
        for _, folders, _ in walk(path):
            if folder in folders:
                return join(path, folder)
        else:
            return find_folder(path=Path(path).parent)

    return find_folder(path=current)


def get_fixtures():
    files_list = []
    for root, dirs, files in walk(get_current_folder(folder='fixtures')):
        for file in files:
            if '.pyc' in file:
                continue
            root_folder = root[root.find('fixtures'):].replace('\\', '.').replace('/', '.')
            file_name = file[:len(file) - 3]
            files_list.append(f'{root_folder}.{file_name}')
    return files_list


def asserts(actual_data: list, asserts_data: list):
    for key, item in enumerate(asserts_data):
        if isinstance(item, dict):
            for value in item.keys():
                if str(value).lower() in dict(actual_data[key]).keys() \
                        and str(value).lower() in dict(asserts_data[key]).keys():
                    assert actual_data[key][str(value).lower()] == asserts_data[key][str(value).lower()], \
                        f'Not found {str(value).lower()} in list {item}'
        elif isinstance(asserts_data[item], dict):
            for data in asserts_data[item]:
                assert actual_data[item][data] == asserts_data[item][data]
        else:
            assert actual_data[item] == asserts_data[item]


def get_path_file_by_name(filename: str) -> str:
    current = getcwd()

    def find_file(path: str or Path) -> str:
        for _, _, files in walk(path):
            if filename in files:
                return join(path, filename)
        else:
            return find_file(path=Path(path).parent)

    return find_file(path=current)

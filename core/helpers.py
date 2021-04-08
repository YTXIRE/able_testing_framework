import json
from os.path import join
from pathlib import Path


def get_settings(environment):
    ROOT_DIR = Path(__file__).parent.parent
    CONFIG_PATH = join(ROOT_DIR, 'config/config.json')
    with open(CONFIG_PATH) as data:
        config = json.load(data)
        return config[environment]

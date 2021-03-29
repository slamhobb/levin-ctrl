import os
import json

_basedir = os.path.abspath(os.path.dirname(__file__))

_config_path = os.path.join(_basedir, '..', 'levin-ctrl-cfg', 'config.json')


def get_config():
    with open(_config_path, 'r') as f:
        return json.load(f)


config = get_config()

from os import path
import json

_basedir = path.abspath(path.dirname(__file__))

_config_path = path.join(_basedir, '..', 'levin-ctrl-cfg', 'config.json')


def get_config():
    with open(_config_path, 'r') as f:
        return json.load(f)


config = get_config()

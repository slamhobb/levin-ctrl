from enum import Enum

import requests
from lib.config import config
from lib.models.relay_data import RelayData
import json

_timeout = 2


class RelayType(Enum):
    RELAY1 = 1
    RELAY2 = 2


class SocketType(Enum):
    SOCKET1 = 1
    SOCKET2 = 2
    SOCKET3 = 3


def get_relay_data(relay_type: RelayType) -> RelayData:
    addr = _get_relay_addr(relay_type)
    url = f'http://{addr}/zeroconf/info'

    request = {'deviceid': '', 'data': {}}

    try:
        response = requests.post(url, json=request, timeout=_timeout).json()

        data = response['data']

        relay_status = data['switch'] == 'on'
        signal_strength = data['signalStrength']
        signal_strength_str = f'{signal_strength} дБ'

        return RelayData(
            relay_status=relay_status,
            signal_strength=signal_strength_str)

    except requests.exceptions.ConnectionError:
        return RelayData(
            relay_status=False,
            signal_strength='Ошибка')


def set_relay(relay_type: RelayType, new_status: bool):
    addr = _get_relay_addr(relay_type)
    url = f'http://{addr}/zeroconf/switch'

    switch_state = 'on' if new_status else 'off'

    request = {'deviceid': '', 'data': {'switch': switch_state}}

    requests.post(url, json=request, timeout=_timeout)


def _get_relay_addr(relay_type: RelayType) -> str:
    if relay_type == RelayType.RELAY1:
        return config['RELAY1_ADDR']

    if relay_type == RelayType.RELAY2:
        return config['RELAY2_ADDR']

    raise Exception('Unsupported relay type')


def set_socket(socket_type: SocketType, new_status: bool):
    (addr, on_data, off_data) = _get_socket_data(socket_type)
    url = f'http://{addr}/zeroconf/switch'
    request = json.loads(on_data if new_status else off_data)

    requests.post(url, json=request, timeout=_timeout)


def _get_socket_data(socket_type: SocketType) -> (str, str, str):
    if socket_type == SocketType.SOCKET1:
        socket = config['SOCKET1']
        return socket['ADDR'], socket['ON_DATA'], socket['OFF_DATA']

    if socket_type == SocketType.SOCKET2:
        socket = config['SOCKET2']
        return socket['ADDR'], socket['ON_DATA'], socket['OFF_DATA']

    if socket_type == SocketType.SOCKET3:
        socket = config['SOCKET3']
        return socket['ADDR'], socket['ON_DATA'], socket['OFF_DATA']

    raise Exception('Unsupported socket type')

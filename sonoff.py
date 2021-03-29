from typing import Tuple
from config import config
import requests

_timeout = 2


def get_relay_data() -> Tuple[bool, str]:
    addr = config['RELAY_ADDR']
    url = f'http://{addr}/zeroconf/info'

    request = {'deviceid': '', 'data': {}}

    try:
        response = requests.post(url, json=request, timeout=_timeout).json()

        data = response['data']

        relay_status = data['switch'] == 'on'
        signal_strength = data['signalStrength']
        signal_strength_str = f'{signal_strength} дБ'

        return relay_status, signal_strength_str

    except requests.exceptions.ConnectionError:
        return False, "Ошибка"


def set_relay(new_status):
    addr = config['RELAY_ADDR']
    url = f'http://{addr}/zeroconf/switch'

    switch_state = 'on' if new_status else 'off'

    request = {'deviceid': '', 'data': {'switch': switch_state}}

    requests.post(url, json=request, timeout=_timeout)

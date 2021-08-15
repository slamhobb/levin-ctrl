import requests
from lib.config import config
from lib.models.relay_data import RelayData

_timeout = 2


def get_relay_data() -> RelayData:
    addr = config['RELAY_ADDR']
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


def set_relay(new_status: bool):
    addr = config['RELAY_ADDR']
    url = f'http://{addr}/zeroconf/switch'

    switch_state = 'on' if new_status else 'off'

    request = {'deviceid': '', 'data': {'switch': switch_state}}

    requests.post(url, json=request, timeout=_timeout)

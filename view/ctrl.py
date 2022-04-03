from infrastructure.parallel import run_parallel

from flask import render_template, redirect, request, Blueprint
from lib.router import get_router_data, set_wifi, set_wifi_ext, set_rule, set_dimaphone_tunnel, set_demkon_tunnel
from lib.sonoff import RelayType, get_relay_data, set_relay
from lib.mqtt import get_devices_data, set_device_state

ctrl = Blueprint('ctrl', __name__)


@ctrl.route('/')
def index():
    results = run_parallel([get_router_data, get_relay_data, get_relay_data],
                           [None, RelayType.RELAY1, RelayType.RELAY2])
    router_data = results[0]
    relay1_data = results[1]
    relay2_data = results[2]
    mqtt_devices_data = get_devices_data()

    return render_template('index.html', router_data=router_data, relay1_data=relay1_data, relay2_data=relay2_data,
                           mqtt_devices_data=mqtt_devices_data)


@ctrl.route('/lights')
def lights():
    relay2_data = get_relay_data(RelayType.RELAY2)

    return render_template('lights.html', relay2_data=relay2_data)


@ctrl.route('/turn-rule', methods=['POST'])
def turn_rule():
    new_status = _bool_parse(request.form['new_status'])
    set_rule(new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-wifi', methods=['POST'])
def turn_wifi():
    new_status = _bool_parse(request.form['new_status'])
    set_wifi(new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-wifi-ext', methods=['POST'])
def turn_wifi_ext():
    new_status = _bool_parse(request.form['new_status'])
    set_wifi_ext(new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-dimaphone-tunnel', methods=['POST'])
def turn_dimaphone_tunnel():
    new_status = _bool_parse(request.form['new_status'])
    set_dimaphone_tunnel(new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-demkon-tunnel', methods=['POST'])
def turn_demkon_tunnel():
    new_status = _bool_parse(request.form['new_status'])
    set_demkon_tunnel(new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-relay1', methods=['POST'])
def turn_relay1():
    new_status = _bool_parse(request.form['new_status'])
    set_relay(RelayType.RELAY1, new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-relay2', methods=['POST'])
def turn_relay2():
    new_status = _bool_parse(request.form['new_status'])
    set_relay(RelayType.RELAY2, new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-mqtt-device', methods=['POST'])
def turn_mqtt_device():
    device_name = request.form['device_name']
    new_state = _bool_parse(request.form['new_status'])
    set_device_state(device_name, new_state)
    return redirect(request.referrer)


def _bool_parse(value: str) -> bool:
    return value.lower() == 'true'

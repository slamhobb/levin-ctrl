import inject

from infrastructure.parallel import run_parallel

from flask import render_template, redirect, request, Blueprint, jsonify, Response
from lib.router import get_router_data, set_wifi, set_wifi_ext, set_rule, set_dimaphone_tunnel, set_demkon_tunnel, \
    set_ipad_tunnel, set_tv_tunnel
from lib.sonoff import RelayType, SocketType, get_relay_data, set_relay, set_socket
from business.mqtt_service import MqttService

ctrl = Blueprint('ctrl', __name__)

mqtt_service = inject.instance(MqttService)


@ctrl.route('/')
def index():
    results = run_parallel([get_router_data, get_relay_data, get_relay_data],
                           [None, RelayType.RELAY1, RelayType.RELAY2])
    router_data = results[0]
    relay1_data = results[1]
    relay2_data = results[2]
    mqtt_devices = mqtt_service.get_devices()

    return render_template('index.html', router_data=router_data, relay1_data=relay1_data, relay2_data=relay2_data,
                           mqtt_devices=mqtt_devices)


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


@ctrl.route('/turn-ipad-tunnel', methods=['POST'])
def turn_ipad_tunnel():
    new_status = _bool_parse(request.form['new_status'])
    set_ipad_tunnel(new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-tv-tunnel', methods=['POST'])
def turn_tv_tunnel():
    new_status = _bool_parse(request.form['new_status'])
    set_tv_tunnel(new_status)
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


@ctrl.route('/turn-socket1', methods=['POST'])
def turn_socket1():
    new_status = _bool_parse(request.form['new_status'])
    set_socket(SocketType.SOCKET1, new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-socket2', methods=['POST'])
def turn_socket2():
    new_status = _bool_parse(request.form['new_status'])
    set_socket(SocketType.SOCKET2, new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-socket3', methods=['POST'])
def turn_socket3():
    new_status = _bool_parse(request.form['new_status'])
    set_socket(SocketType.SOCKET3, new_status)
    return redirect(request.referrer)


@ctrl.route('/turn-mqtt-switch', methods=['POST'])
def turn_mqtt_switch():
    device_name = request.form['device_name']
    new_state = _bool_parse(request.form['new_state'])
    mqtt_service.set_switch_device_state(device_name, new_state)

    if request.referrer is None:
        return Response(status=200)

    return redirect(request.referrer)


@ctrl.route('/get-mqtt-device', methods=['POST'])
def get_mqtt_device():
    device_name = request.form['device_name']
    device = mqtt_service.get_device(device_name)
    return jsonify(device.__dict__)


@ctrl.route('/set-mqtt-motor', methods=['POST'])
def set_mqtt_motor():
    device_name = request.form['device_name']
    position = request.form['position']
    mqtt_service.set_device_state(device_name, dict(position=position))

    if request.referrer is None:
        return Response(status=200)

    return redirect(request.referrer)


def _bool_parse(value: str) -> bool:
    return value.lower() == 'true'

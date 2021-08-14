from flask import render_template, redirect, url_for, request, Blueprint
from lib.router import get_router_data, set_wifi, set_wifi_ext, set_rule, set_dimaphone_tunnel
from lib.sonoff import get_relay_data, set_relay

ctrl = Blueprint('ctrl', __name__)


@ctrl.route('/')
def index():
    rule_status, wifi_status, \
     wifi_lines, wifi_ext_status, \
     dimaphone_tunnel_status = get_router_data()

    relay_status, signal_strength = get_relay_data()

    return render_template('index.html', rule_status=rule_status,
                           wifi_status=wifi_status, wifi_lines=wifi_lines,
                           wifi_ext_status=wifi_ext_status, dimaphone_tunnel_status=dimaphone_tunnel_status,
                           relay_status=relay_status, signal_strength=signal_strength)


@ctrl.route('/turn-rule', methods=['POST'])
def turn_rule():
    new_status = _bool_parse(request.form['new_status'])
    set_rule(new_status)
    return redirect(url_for('.index'))


@ctrl.route('/turn-wifi', methods=['POST'])
def turn_wifi():
    new_status = _bool_parse(request.form['new_status'])
    set_wifi(new_status)
    return redirect(url_for('.index'))


@ctrl.route('/turn-wifi-ext', methods=['POST'])
def turn_wifi_ext():
    new_status = _bool_parse(request.form['new_status'])
    set_wifi_ext(new_status)
    return redirect(url_for('.index'))


@ctrl.route('/turn-dimaphone-tunnel', methods=['POST'])
def turn_dimaphone_tunnel():
    new_status = _bool_parse(request.form['new_status'])
    set_dimaphone_tunnel(new_status)
    return redirect(url_for('.index'))


@ctrl.route('/turn-relay', methods=['POST'])
def turn_relay():
    new_status = _bool_parse(request.form['new_status'])
    set_relay(new_status)
    return redirect(url_for('.index'))


def _bool_parse(value: str) -> bool:
    return value.lower() == 'true'

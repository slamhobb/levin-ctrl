from flask import render_template, redirect, url_for, request, Blueprint
from lib.router import get_router_data, set_wifi, set_wifi_ext, set_rule, set_dimaphone_tunnel, set_demkon_tunnel
from lib.sonoff import get_relay_data, set_relay

ctrl = Blueprint('ctrl', __name__)


@ctrl.route('/')
def index():
    router_data = get_router_data()
    relay_data = get_relay_data()

    return render_template('index.html', router_data=router_data, relay_data=relay_data)


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


@ctrl.route('/turn-demkon-tunnel', methods=['POST'])
def turn_demkon_tunnel():
    new_status = _bool_parse(request.form['new_status'])
    set_demkon_tunnel(new_status)
    return redirect(url_for('.index'))


@ctrl.route('/turn-relay', methods=['POST'])
def turn_relay():
    new_status = _bool_parse(request.form['new_status'])
    set_relay(new_status)
    return redirect(url_for('.index'))


def _bool_parse(value: str) -> bool:
    return value.lower() == 'true'

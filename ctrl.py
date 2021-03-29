from flask import render_template, redirect, url_for, request, Blueprint
from router import get_data, set_wifi, set_wifi_ext, set_rule

ctrl = Blueprint("ctrl", __name__)


@ctrl.route("/")
def index():
    rule_status, wifi_status, \
     wifi_lines, wifi_ext_status = get_data()

    return render_template("index.html", rule_status=rule_status,
                           wifi_status=wifi_status, wifi_lines=wifi_lines,
                           wifi_ext_status=wifi_ext_status)


@ctrl.route("/turn-rule", methods=["POST"])
def turn_rule():
    new_status = _bool_parse(request.form["new_status"])
    set_rule(new_status)
    return redirect(url_for('.index'))


@ctrl.route("/turn-wifi", methods=["POST"])
def turn_wifi():
    new_status = _bool_parse(request.form["new_status"])
    set_wifi(new_status)
    return redirect(url_for('.index'))


@ctrl.route("/turn-wifi-ext", methods=["POST"])
def turn_wifi_ext():
    new_status = _bool_parse(request.form["new_status"])
    set_wifi_ext(new_status)
    return redirect(url_for('.index'))


def _bool_parse(value: str) -> bool:
    return value.lower() == 'true'

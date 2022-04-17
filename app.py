from dependency_injection import configure_inject
configure_inject()

import inject

from flask import Flask

from view.ctrl import ctrl
from view.log import log
from view.black import black

from business.mqtt_service import MqttService
from lib.mqtt import run_mqtt


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ctrl, url_prefix='/ctrl')
    app.register_blueprint(log, url_prefix='/ctrl/log')
    app.register_blueprint(black, url_prefix='/ctrl/black')

    mqtt_service = inject.instance(MqttService)

    run_mqtt(mqtt_service.on_connect, mqtt_service.on_disconnect, mqtt_service.on_message)

    return app

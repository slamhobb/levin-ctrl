from collections.abc import Callable

import json

import paho.mqtt.client as mqtt

from lib.config import config

_on_connect_func: Callable[[object], [str]]
_on_disconnect_func: Callable[[], None]
_on_message_func: Callable[[str, dict], None]


def run_mqtt(on_connect: Callable[[object], [str]],
             on_disconnect: Callable[[str, dict], None],
             on_message: Callable[[str, dict], None]):
    global _on_connect_func
    global _on_disconnect_func
    global _on_message_func

    _on_connect_func = on_connect
    _on_disconnect_func = on_disconnect
    _on_message_func = on_message

    client = mqtt.Client()
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.on_disconnect = _on_disconnect

    client.connect(config["MQTT"]["SERVER_ADDR"], 1883, 60)

    client.loop_start()


def _on_connect(client, userdata, flags, rc):
    if rc != 0:
        return

    topics = _on_connect_func(client)

    for topic in topics:
        client.subscribe(topic)


def _on_disconnect(client, userdata, rc):
    _on_disconnect_func()


def _on_message(client, userdata, msg):
    device_name = msg.topic
    payload = json.loads(msg.payload)

    _on_message_func(device_name, payload)

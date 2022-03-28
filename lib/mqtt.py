from typing import List

import json

import paho.mqtt.client as mqtt

from lib.config import config
from lib.models.mqtt_data import MqttData, MqttDeviceData

mqtt_client: mqtt.Client

mqtt_state = MqttData(
    connected=False,
    devices={})


def run_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config["MQTT"]["SERVER_ADDR"], 1883, 60)

    device_topics = config["MQTT"]["DEVICE_TOPICS"]

    for topic in device_topics:
        mqtt_state.devices[topic] = MqttDeviceData(name=topic, state=False, signal_strength='Неизвестно')

        client.subscribe(topic)

    client.loop_start()

    global mqtt_client
    mqtt_client = client


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        mqtt_state.connected = True


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)

    state = payload['state'].lower() == "on"
    signal_strength = payload['linkquality']
    signal_strength_str = f'{signal_strength} дБ'

    device_name = msg.topic
    device_data = MqttDeviceData(name=device_name, state=state, signal_strength=signal_strength_str)

    mqtt_state.devices[device_name] = device_data


def get_devices_data() -> List[MqttDeviceData]:
    return [value for value in mqtt_state.devices.values()]


def set_device_state(device_name, new_state):
    device = mqtt_state.devices.get(device_name, None)
    device_state = 'ON' if new_state else 'OFF'

    if device is not None:
        mqtt_client.publish(f'{device.name}/set', device_state)

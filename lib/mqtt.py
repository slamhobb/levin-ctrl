from typing import List

import json

import paho.mqtt.client as mqtt

from lib.config import config
from lib.models.mqtt_data import MqttData, MqttDevice, DeviceType
from lib.mqtt_device_mapper import map_device

mqtt_client: mqtt.Client

mqtt_state = MqttData(
    connected=False,
    devices={}
)


def run_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(config["MQTT"]["SERVER_ADDR"], 1883, 60)

    client.loop_start()

    global mqtt_client
    mqtt_client = client


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        return

    mqtt_state.connected = True

    for device_config in config["MQTT"]["DEVICES"]:
        topic = device_config['TOPIC']
        device_type = DeviceType(device_config['TYPE'])

        device = map_device(topic, device_type, {})
        if device is not None:
            mqtt_state.devices[topic] = device

        client.subscribe(topic)


def on_disconnect(client, userdata, rc):
    mqtt_state.connected = False
    mqtt_state.devices = {}


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)

    device_name = msg.topic
    old_device = mqtt_state.devices[device_name]

    mqtt_state.devices[device_name] = map_device(device_name, old_device.type, payload)


def get_devices() -> List[MqttDevice]:
    return [device for device in mqtt_state.devices.values()]


def get_device(device_name: str) -> MqttDevice:
    return mqtt_state.devices.get(device_name, None)


def set_switch_device_state(device_name, new_state):
    device = mqtt_state.devices.get(device_name, None)
    if device is None or device.type != DeviceType.SWITCH:
        return

    device_state = 'ON' if new_state else 'OFF'
    mqtt_client.publish(f'{device.name}/set', device_state)

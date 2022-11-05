import inject

from lib.config import config
from lib.models.mqtt_data import MqttData, DeviceType, MqttDevice
from business.mqtt_device_mapper import MqttDeviceMapper
from business.smart_light_logic_service import SmartLightLogicService
from business.smart_socket_logic_service import SmartSocketLogicService
from business.light_repeater_service import LightRepeaterService


class MqttService:
    smart_light_logic_service = inject.attr(SmartLightLogicService)
    smart_socket_logic_service = inject.attr(SmartSocketLogicService)
    light_repeater_service = inject.attr(LightRepeaterService)

    def __init__(self):
        self.mqtt_client = None
        self.mqtt_state = MqttData(
            connected=False,
            # device by topic
            devices={}
        )

    def on_connect(self, mqtt_client: object) -> [str]:
        self.mqtt_client = mqtt_client
        self.mqtt_state.connected = True

        topics = []
        for device_config in config['MQTT']['DEVICES']:
            topic = device_config['TOPIC']
            device_type = DeviceType(device_config['TYPE'])
            device_name = device_config['NAME']

            device = MqttDeviceMapper.map_device(device_name, device_type, {})
            if device is not None:
                self.mqtt_state.devices[topic] = device
                topics.append(topic)

        return topics

    def on_disconnect(self):
        self.mqtt_state.connected = False
        self.mqtt_state.devices = {}

    def on_message(self, topic: str, payload: dict):
        old_device = self.mqtt_state.devices.get(topic, None)
        if old_device is None:
            return

        new_device = MqttDeviceMapper.map_device(old_device.name, old_device.type, payload)
        self.mqtt_state.devices[topic] = new_device

        if old_device.is_equal(new_device):
            return

        self.smart_light_logic_service.on_change_device(new_device, self.set_switch_device_state, self.get_device)
        self.smart_socket_logic_service.on_change_device(new_device, self.set_switch_device_state)
        self.light_repeater_service.on_change_device(new_device, self.set_switch_device_state)

    def get_devices(self) -> [MqttDevice]:
        return [device for device in self.mqtt_state.devices.values()]

    def get_device(self, device_name: str) -> MqttDevice:
        topic = self._get_topic_by_device_name(device_name)
        return self.mqtt_state.devices.get(topic, None)

    def set_switch_device_state(self, device_name: str, new_state: bool):
        topic = self._get_topic_by_device_name(device_name)
        device = self.mqtt_state.devices.get(topic, None)
        switch_device_types = [DeviceType.SWITCH, DeviceType.SOCKET]

        if device is None or device.type not in switch_device_types:
            return

        device_state = 'ON' if new_state else 'OFF'
        self.mqtt_client.publish(f'{topic}/set', device_state)

    @staticmethod
    def _get_topic_by_device_name(device_name: str) -> str:
        devices = [device_config for device_config in config['MQTT']['DEVICES'] if device_config['NAME'] == device_name]
        return devices[0]['TOPIC']

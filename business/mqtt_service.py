from lib.config import config
from lib.models.mqtt_data import MqttData, DeviceType, MqttDevice
from business.mqtt_device_mapper import MqttDeviceMapper
from business.smart_home_logic_service import SmartHomeLogicService


class MqttService:
    def __init__(self):
        self.mqtt_client = None
        self.mqtt_state = MqttData(
            connected=False,
            devices={}
        )

    def on_connect(self, mqtt_client: object) -> [str]:
        self.mqtt_client = mqtt_client
        self.mqtt_state.connected = True

        topics = []
        for device_config in config["MQTT"]["DEVICES"]:
            device_name = device_config['TOPIC']
            device_type = DeviceType(device_config['TYPE'])

            device = MqttDeviceMapper.map_device(device_name, device_type, {})
            if device is not None:
                self.mqtt_state.devices[device_name] = device
                topics.append(device_name)

        return topics

    def on_disconnect(self):
        self.mqtt_state.connected = False
        self.mqtt_state.devices = {}

    def on_message(self, device_name: str, payload: dict):
        old_device = self.mqtt_state.devices.get(device_name, None)
        if old_device is None:
            return

        new_device = MqttDeviceMapper.map_device(device_name, old_device.type, payload)
        self.mqtt_state.devices[device_name] = new_device

        if not old_device.is_equal(new_device):
            SmartHomeLogicService.on_change_device(new_device, self.set_switch_device_state)

    def get_devices(self) -> [MqttDevice]:
        return [device for device in self.mqtt_state.devices.values()]

    def get_device(self, device_name: str) -> MqttDevice:
        return self.mqtt_state.devices.get(device_name, None)

    def set_switch_device_state(self, device_name: str, new_state: bool):
        device = self.mqtt_state.devices.get(device_name, None)
        if device is None or device.type != DeviceType.SWITCH:
            return

        device_state = 'ON' if new_state else 'OFF'
        self.mqtt_client.publish(f'{device.name}/set', device_state)

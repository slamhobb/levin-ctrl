from collections.abc import Callable

from lib.models.mqtt_data import DeviceType, MqttDevice


class SmartHomeLogicService:
    @staticmethod
    def on_change_device(device: MqttDevice, set_switch_device_state: Callable[[str, bool], None]):
        if device.name == 'Датчик движения' and device.type == DeviceType.MOTION:
            light_new_state = device.occupancy
            set_switch_device_state('Лампочка кухня', light_new_state)

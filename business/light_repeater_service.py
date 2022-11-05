from collections.abc import Callable

from lib.models.mqtt_data import DeviceType, MqttDevice


class LightRepeaterService:
    def on_change_device(
            self,
            device: MqttDevice,
            set_switch_device_state: Callable[[str, bool], None]
    ):
        if device.name == 'Лампочка зал' and device.type == DeviceType.SWITCH:
            set_switch_device_state('Лампочка зал-1', device.state)
            set_switch_device_state('Лампочка зал-2', device.state)

from collections.abc import Callable

from lib.models.mqtt_data import DeviceType, MqttDevice


class LightRepeaterService:
    def on_change_device(
            self,
            device: MqttDevice,
            set_device_state: Callable[[str, dict], None]
    ):
        if device.name == 'Лампочка зал' and device.type == DeviceType.LIGHT:
            state = 'ON' if device.state else 'OFF'

            set_device_state('Лампочка зал-1', dict(state=state, brightness=device.brightness,
                                                    color_temp=device.color_temp))
            set_device_state('Лампочка зал-2', dict(state=state, brightness=device.brightness,
                                                    color_temp=device.color_temp))

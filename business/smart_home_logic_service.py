from collections.abc import Callable

from threading import Timer
from datetime import datetime, timedelta

from lib.models.mqtt_data import DeviceType, MqttDevice

MINUTES_TURN_LIGHT = 30


class SmartHomeLogicService:
    def __init__(self):
        self.timer = None
        self.off_time = None

    def on_change_device(self, device: MqttDevice, set_switch_device_state: Callable[[str, bool], None]):
        if device.name == 'Датчик движения' and device.type == DeviceType.MOTION:
            self._on_motion(device.occupancy, set_switch_device_state)

        if device.name == 'Кнопка 1' and device.type == DeviceType.BUTTON:
            self._on_button(device.action, set_switch_device_state)

    def _on_motion(self, occupancy: bool, set_switch_device_state: Callable[[str, bool], None]):
        light_new_state = occupancy

        if light_new_state is False and \
                self.off_time is not None and \
                datetime.now() < self.off_time:
            return

        set_switch_device_state('Лампочка кухня', light_new_state)

    def _on_button(self, action: str, set_switch_device_state: Callable[[str, bool], None]):
        if action == 'single':
            if self.timer is not None:
                self.timer.cancel()

            self.timer = Timer(MINUTES_TURN_LIGHT * 60, lambda: self._deferred_light_off(set_switch_device_state))
            self.timer.start()

            self.off_time = datetime.now() + timedelta(minutes=MINUTES_TURN_LIGHT)
            set_switch_device_state('Лампочка кухня', True)

        if action == 'double':
            if self.timer is not None:
                self.timer.cancel()

            self.off_time = None
            set_switch_device_state('Лампочка кухня', False)

    def _deferred_light_off(self, set_switch_device_state: Callable[[str, bool], None]):
        self.off_time = None
        set_switch_device_state('Лампочка кухня', False)

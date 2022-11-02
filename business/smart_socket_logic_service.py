from collections.abc import Callable

from threading import Timer

from lib.config import config

from lib.models.mqtt_data import DeviceType, MqttDevice

WORK_POWER = 7.0


class SmartSocketLogicService:
    def __init__(self):
        self.timer = None

    def on_change_device(
            self,
            device: MqttDevice,
            set_switch_device_state: Callable[[str, bool], None]
    ):
        if device.name != 'Розетка' or device.type != DeviceType.SOCKET:
            return

        if device.state and device.power >= config['SOCKET_MIN_WATT']:
            self._on_socket_work_power()

        if device.state and device.power < config['SOCKET_MIN_WATT']:
            self._on_socket_less_work_power(set_switch_device_state)

        if not device.state:
            self._on_socket_turn_off()

    def _on_socket_work_power(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def _on_socket_less_work_power(
            self,
            set_switch_device_state: Callable[[str, bool], None]
    ):
        if self.timer is not None:
            return

        self.timer = Timer(config['MINUTES_TURN_OFF_SOCKET'] * 60,
                           lambda: self._deferred_socket_off(set_switch_device_state))
        self.timer.start()

    def _on_socket_turn_off(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def _deferred_socket_off(
            self,
            set_switch_device_state: Callable[[str, bool], None]
    ):
        set_switch_device_state('Розетка', False)

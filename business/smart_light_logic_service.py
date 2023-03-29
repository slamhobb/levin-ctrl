import inject

from collections.abc import Callable

from threading import Timer
from datetime import datetime, timedelta

from lib.config import config

from lib.models.mqtt_data import DeviceType, MqttDevice
from business.twilight_time_service import TwilightTimeService


class SmartLightLogicService:
    twilight_time_service = inject.attr(TwilightTimeService)

    def __init__(self):
        self.timer = None
        self.off_time = None

    def on_change_device(
            self,
            device: MqttDevice,
            set_switch_device_state: Callable[[str, bool], None],
            get_device: Callable[[str], MqttDevice]
    ):
        if (device.name == 'Датчик движения'
            or device.name == 'Датчик движения 2'
            or device.name == 'Датчик движения 3')\
                and device.type == DeviceType.MOTION:
            self._on_motion(device.occupancy, get_device, set_switch_device_state)

        if device.name == 'Кнопка 1' and device.type == DeviceType.BUTTON:
            self._on_button(device.action, get_device, set_switch_device_state)

    def _on_motion(
            self,
            occupancy: bool,
            get_device: Callable[[str], MqttDevice],
            set_switch_device_state: Callable[[str, bool], None]
    ):
        if occupancy:
            self._on_motion_start(set_switch_device_state)
        else:
            self._on_motion_end(get_device, set_switch_device_state)

    def _on_motion_start(
            self,
            set_switch_device_state: Callable[[str, bool], None]
    ):
        if self.twilight_time_service.is_light_now():
            return

        set_switch_device_state('Лампочка кухня', True)

    def _on_motion_end(
            self,
            get_device: Callable[[str], MqttDevice],
            set_switch_device_state: Callable[[str, bool], None]
    ):
        occupancy1 = get_device('Датчик движения').occupancy
        occupancy2 = get_device('Датчик движения 2').occupancy
        occupancy3 = get_device('Датчик движения 3').occupancy

        off_light = not occupancy1 and not occupancy2 and not occupancy3
        if not off_light:
            return

        if self.off_time is not None \
                and datetime.now() < self.off_time:
            return

        set_switch_device_state('Лампочка кухня', False)

    def _on_button(
            self,
            action: str,
            get_device: Callable[[str], MqttDevice],
            set_switch_device_state: Callable[[str, bool], None]
    ):
        if action == 'single':
            if self.timer is not None:
                self.timer.cancel()

            self.timer = Timer(config['MINUTES_TURN_LIGHT'] * 60,
                               lambda: self._deferred_light_off(get_device, set_switch_device_state))
            self.timer.start()

            self.off_time = datetime.now() + timedelta(minutes=config['MINUTES_TURN_LIGHT'])
            set_switch_device_state('Лампочка кухня', True)

        if action == 'double':
            if self.timer is not None:
                self.timer.cancel()

            self.off_time = None
            set_switch_device_state('Лампочка кухня', False)

    def _deferred_light_off(
            self,
            get_device: Callable[[str], MqttDevice],
            set_switch_device_state: Callable[[str, bool], None]
    ):
        self.off_time = None

        occupancy1 = get_device('Датчик движения').occupancy
        occupancy2 = get_device('Датчик движения 2').occupancy
        occupancy3 = get_device('Датчик движения 3').occupancy

        off_light = not occupancy1 and not occupancy2 and not occupancy3
        if off_light:
            set_switch_device_state('Лампочка кухня', False)

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class DeviceType(str, Enum):
    SWITCH = 'switch'
    SOCKET = 'socket'
    LIGHT = 'light'
    TEMP_HUM = 'temp_hum'
    BUTTON = 'button'
    MOTION = 'motion'


@dataclass
class MqttDevice:
    name: str
    type: DeviceType
    signal_strength: str

    def is_equal(self, device: MqttDevice):
        excepted_fields = ['signal_strength']
        dict1 = {k: v for k, v in self.__dict__.items() if k not in excepted_fields}
        dict2 = {k: v for k, v in device.__dict__.items() if k not in excepted_fields}
        return dict1 == dict2


@dataclass
class MqttBatteryDevice:
    battery: int = 0
    voltage: int = 0


@dataclass
class MqttDeviceSwitch(MqttDevice):
    state: bool = False


@dataclass
class MqttDeviceSocket(MqttDeviceSwitch):
    power: float = 0.0


@dataclass
class MqttDeviceLight(MqttDeviceSwitch):
    brightness: int = 0
    color_temp: int = 0


@dataclass
class MqttDeviceTempHum(MqttBatteryDevice, MqttDevice):
    temperature: float = 0.0
    humidity: float = 0.0


@dataclass
class MqttDeviceButton(MqttBatteryDevice, MqttDevice):
    action: str = ''


@dataclass
class MqttDeviceMotion(MqttBatteryDevice, MqttDevice):
    occupancy: bool = False


@dataclass
class MqttData:
    connected: bool
    devices: dict[str, MqttDevice]

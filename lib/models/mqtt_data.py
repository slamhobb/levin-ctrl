from typing import Dict
from dataclasses import dataclass
from enum import Enum


class DeviceType(str, Enum):
    SWITCH = 'switch'
    TEMP_HUM = 'temp_hum'


@dataclass
class MqttDevice:
    name: str
    type: DeviceType
    signal_strength: str


@dataclass
class MqttDeviceSwitch(MqttDevice):
    state: bool = False


@dataclass
class MqttDeviceTempHum(MqttDevice):
    temperature: float = 0.0
    humidity: float = 0.0
    battery: int = 0
    voltage: int = 0


@dataclass
class MqttData:
    connected: bool
    devices: Dict[str, MqttDevice]

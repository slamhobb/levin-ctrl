from dataclasses import dataclass
from typing import Dict


@dataclass
class MqttDeviceData:
    name: str
    state: bool
    signal_strength: str


@dataclass
class MqttData:
    connected: bool
    devices: Dict[str, MqttDeviceData]

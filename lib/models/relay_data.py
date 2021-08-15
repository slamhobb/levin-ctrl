from dataclasses import dataclass


@dataclass
class RelayData:
    relay_status: bool
    signal_strength: str

from dataclasses import dataclass


@dataclass
class RouterData:
    rule_status: bool
    wifi_status: bool
    wifi_lines: [str]
    wifi_ext_status: bool
    dimaphone_tunnel_status: bool
    demkon_tunnel_status: bool
    ipad_tunnel_status: bool

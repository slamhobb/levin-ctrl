from typing import List, Tuple
import subprocess as sp
from enum import Enum
from config import config


class RouterType(Enum):
    MAIN = 1
    WIFI = 2


def get_data():
    command1 = ' '.join([
        ':if [/system scheduler get turnoff-wifi disabled] do= { :put false } else= { :put true };',
        ':if [/interface get wlan1 disabled] do= { :put false } else= { :put true };',
        '/interface wireless registration-table print'
    ])

    command2 = ':if [/interface get wlan1 disabled] do= { :put false } else= { :put true };'

    queries = [
        (command1, RouterType.WIFI),
        (command2, RouterType.MAIN)
    ]

    [result1, result2] = _ssh_multi_query(queries)

    lines = result1.split('\n')

    rule_status = lines.pop(0)
    rule_status = rule_status == 'true'

    wifi_status = lines.pop(0)
    wifi_status = wifi_status == 'true'

    wifi_lines = lines

    wifi_ext_status = result2.split('\n')[0] == 'true'

    return rule_status, wifi_status, wifi_lines, wifi_ext_status


def set_wifi(new_status):
    disabled = 'no' if new_status else 'yes'
    _ssh_query(f'/interface wireless set wlan1 disabled={disabled}', RouterType.WIFI)


def set_rule(new_status):
    disabled = 'no' if new_status else 'yes'
    _ssh_query(f'/system scheduler set turnoff-wifi disabled={disabled}', RouterType.WIFI)


def set_wifi_ext(new_status):
    disabled = 'no' if new_status else 'yes'
    _ssh_query(f'/interface wireless set wlan1 disabled={disabled}', RouterType.MAIN)


def _ssh_query(query: str, router_type: RouterType) -> str:
    cmd = _build_command(query, router_type)
    return sp.getoutput(cmd)


def _ssh_multi_query(queries: List[Tuple[str, RouterType]]) -> List[str]:
    cmds = [_build_command(query, router_type) for (query, router_type) in queries]

    processes = [sp.Popen(cmd, shell=True, stdout=sp.PIPE, universal_newlines=True) for cmd in cmds]

    for p in processes:
        p.wait()

    results = [p.communicate()[0] for p in processes]

    return results


def _build_command(query: str, router_type: RouterType) -> str:
    if router_type == RouterType.MAIN:
        addr = config['MAIN_ROUTER_ADDR']
        pwd = config['MAIN_ROUTER_PASSWD']
        return f"sshpass -p '{pwd}' ssh {addr} '{query}'"

    if router_type == RouterType.WIFI:
        addr = config['WIFI_ROUTER_ADDR']
        pwd = config['WIFI_ROUTER_PASSWD']
        return f"sshpass -p '{pwd}' ssh {addr} '{query}'"

    raise Exception(f'Unsupported RouterType = {router_type}')

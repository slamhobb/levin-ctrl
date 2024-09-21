from enum import Enum
import subprocess as sp
from lib.config import config
from lib.models.router_data import RouterData


class RouterType(Enum):
    MAIN = 1
    WIFI = 2


def get_router_data() -> RouterData:
    command1 = ' '.join([
        ':if [/system scheduler get turnoff-wifi disabled] do= { :put false } else= { :put true };',
        ':if [/interface get wlan1 disabled] do= { :put false } else= { :put true };',
        '/interface wireless registration-table print;',
    ])

    command2 = ''.join([
        ':if [/interface get wlan1 disabled] do= { :put false } else= { :put true };',
        ':if [/ip firewall mangle get [find comment="traffic from DimaPhone to ISP1"] disabled] do= { :put true } else= { :put false };',
        ':if [/ip firewall mangle get [find comment="traffic from Demkon to ISP1"] disabled] do= { :put true } else= { :put false };',
        ':if [/ip firewall mangle get [find comment="traffic from iPad to ISP1"] disabled] do= { :put true } else= { :put false };',
        ':if [/ip firewall mangle get [find comment="traffic from TV to ISP1"] disabled] do= { :put true } else= { :put false };'
    ])

    queries = [
        (command1, RouterType.WIFI),
        (command2, RouterType.MAIN)
    ]

    [result1, result2] = _ssh_multi_query(queries)

    lines1 = result1.split('\n')

    rule_status = lines1.pop(0)
    rule_status = rule_status == 'true'

    wifi_status = lines1.pop(0)
    wifi_status = wifi_status == 'true'

    wifi_lines = lines1

    lines2 = result2.split('\n')

    wifi_ext_status = lines2.pop(0)
    wifi_ext_status = wifi_ext_status == 'true'

    dimaphone_tunnel_status = lines2.pop(0)
    dimaphone_tunnel_status = dimaphone_tunnel_status == 'true'

    demkon_tunnel_status = lines2.pop(0)
    demkon_tunnel_status = demkon_tunnel_status == 'true'

    ipad_tunnel_status = lines2.pop(0)
    ipad_tunnel_status = ipad_tunnel_status == 'true'

    tv_tunnel_status = lines2.pop(0)
    tv_tunnel_status = tv_tunnel_status == 'true'

    return RouterData(
        rule_status=rule_status,
        wifi_status=wifi_status,
        wifi_lines=wifi_lines,
        wifi_ext_status=wifi_ext_status,
        dimaphone_tunnel_status=dimaphone_tunnel_status,
        demkon_tunnel_status=demkon_tunnel_status,
        ipad_tunnel_status=ipad_tunnel_status,
        tv_tunnel_status=tv_tunnel_status)


def set_wifi(new_status: bool):
    disabled = 'no' if new_status else 'yes'
    _ssh_query(f'/interface wireless set wlan1 disabled={disabled}', RouterType.WIFI)


def set_rule(new_status: bool):
    disabled = 'no' if new_status else 'yes'
    _ssh_query(f'/system scheduler set turnoff-wifi disabled={disabled}', RouterType.WIFI)


def set_wifi_ext(new_status: bool):
    disabled = 'no' if new_status else 'yes'
    _ssh_query(f'/interface wireless set wlan1 disabled={disabled}', RouterType.MAIN)


def set_dimaphone_tunnel(new_status: bool):
    disabled = 'yes' if new_status else 'no'
    _ssh_query(f'/ip firewall mangle set [find comment="traffic from DimaPhone to ISP1"] disabled={disabled}', RouterType.MAIN)
    _ssh_query('/ip firewall connection remove [find src-address~"192.168.88.105"];', RouterType.MAIN)


def set_demkon_tunnel(new_status: bool):
    disabled = 'yes' if new_status else 'no'
    _ssh_query(f'/ip firewall mangle set [find comment="traffic from Demkon to ISP1"] disabled={disabled}', RouterType.MAIN)
    _ssh_query('/ip firewall connection remove [find src-address~"192.168.88.103"];', RouterType.MAIN)


def set_ipad_tunnel(new_status: bool):
    disabled = 'yes' if new_status else 'no'
    _ssh_query(f'/ip firewall mangle set [find comment="traffic from iPad to ISP1"] disabled={disabled}', RouterType.MAIN)
    _ssh_query('/ip firewall connection remove [find src-address~"192.168.88.101"];', RouterType.MAIN)


def set_tv_tunnel(new_status: bool):
    disabled = 'yes' if new_status else 'no'
    _ssh_query(f'/ip firewall mangle set [find comment="traffic from TV to ISP1"] disabled={disabled}', RouterType.MAIN)
    _ssh_query('/ip firewall connection remove [find src-address~"192.168.88.133"];', RouterType.MAIN)


def get_black_list() -> [str]:
    result = _ssh_query('/ip firewall address-list print where list=NginxBanList', RouterType.MAIN)
    return result.split('\n')


def _ssh_query(query: str, router_type: RouterType) -> str:
    cmd = _build_command(query, router_type)
    return sp.getoutput(cmd)


def _ssh_multi_query(queries: [(str, RouterType)]) -> [str]:
    cmds = [_build_command(query, router_type) for (query, router_type) in queries]

    processes = [sp.Popen(cmd, shell=True, stdout=sp.PIPE, universal_newlines=True) for cmd in cmds]

    for p in processes:
        p.wait()

    results = [p.communicate()[0] for p in processes]

    return results


def _build_command(query: str, router_type: RouterType) -> str:
    if router_type == RouterType.MAIN:
        addr = config['MAIN_ROUTER_ADDR']
        return f"ssh {addr} '{query}'"

    if router_type == RouterType.WIFI:
        addr = config['WIFI_ROUTER_ADDR']
        return f"ssh {addr} '{query}'"

    raise Exception(f'Unsupported RouterType = {router_type}')

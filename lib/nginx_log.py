from typing import List
from enum import Enum
import subprocess as sp
from lib.config import config


class LogType(Enum):
    IP = 1
    STATUS_40x = 2
    PHP = 3


def get_log(log_type: LogType) -> List[str]:
    if log_type == LogType.IP:
        return get_ip_log()
    if log_type == LogType.STATUS_40x:
        return get_40x_log()
    if log_type == LogType.PHP:
        return get_php_log()


LOG_FOLDER = '/var/log/nginx'


def get_ip_log() -> List[str]:
    cmd = _get_logs_cmd()
    cmd += " | awk '{print $1}' | sort | uniq -c | sort -rn"
    return _exec_command(cmd)


def get_40x_log() -> List[str]:
    cmd = _get_logs_cmd()
    cmd += " | awk '($9 ~ /40./)' | awk '{print $9, $1, $7}' | sort | uniq -c | sort -rn"
    return _exec_command(cmd)


def get_php_log() -> List[str]:
    cmd = _get_logs_cmd()
    cmd += " | awk '($7 ~ /php/)' | awk '{print $1, $7}' | sort | uniq -c | sort -rn"
    return _exec_command(cmd)


def _get_logs_cmd() -> str:
    log_path = config["NGINX_LOG_PATH"]
    return f"cat {log_path}/access.log {log_path}/access.log.1"


def _exec_command(cmd: str) -> List[str]:
    result = sp.getoutput(cmd)
    return result.split('\n')

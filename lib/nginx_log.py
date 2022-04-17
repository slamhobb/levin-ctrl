from enum import Enum
import subprocess as sp
from lib.config import config


class LogType(Enum):
    IP = 1
    STATUS = 2
    URL = 3


def get_log(log_type: LogType, param: str) -> [str]:
    if log_type == LogType.IP:
        return get_ip_log()
    if log_type == LogType.STATUS:
        return get_status_log(param)
    if log_type == LogType.URL:
        return get_url_log(param)


LOG_FOLDER = '/var/log/nginx'


def get_ip_log() -> [str]:
    cmd = _get_logs_cmd()
    total = _exec(cmd + " | awk '{print $1}' | sort | uniq -c | sort -rn")
    return _union(total, [])


def get_status_log(status) -> [str]:
    cmd = _get_logs_cmd()
    total = _exec(cmd + f" | awk '($9 ~ /{status}/)' | " + "awk '{print $9, $1}' | sort | uniq -c | sort -rn")
    detail = _exec(cmd + f" | awk '($9 ~ /{status}/)' | " + "awk '{print $9, $1, $7}' | sort | uniq -c | sort -rn")
    return _union(total, detail)


def get_url_log(url) -> [str]:
    cmd = _get_logs_cmd()
    total = _exec(cmd + f" | awk '($7 ~ /{url}/)' | " + "awk '{print $1}' | sort | uniq -c | sort -rn")
    detail = _exec(cmd + f" | awk '($7 ~ /{url}/)' | " + "awk '{print $1, $7}' | sort | uniq -c | sort -rn")
    return _union(total, detail)


def _get_logs_cmd() -> str:
    log_path = config["NGINX_LOG_PATH"]
    return f"cat {log_path}/access.log {log_path}/access.log.1"


def _exec(cmd: str) -> [str]:
    result = sp.getoutput(cmd)
    return result.split('\n')


def _union(total: [str], detail: [str]) -> [str]:
    if len(detail) == 0:
        return total

    result = []
    result.extend(total)
    total.extend(['-------'])
    total.extend(detail)
    return total

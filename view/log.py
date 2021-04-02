from flask import render_template, Blueprint, request
from lib.nginx_log import LogType, get_log

log = Blueprint('log', __name__)


@log.route('/')
def index():
    log_type = int(request.args.get('log_type', LogType.IP.value))
    param = request.args.get('param', '')

    log_type = LogType(log_type)
    log_lines = get_log(log_type, param)

    return render_template('log.html', LogType=LogType, log_type=log_type, param=param, log_lines=log_lines)

from flask import render_template, Blueprint
from lib.nginx_log import LogType, get_log

log = Blueprint('log', __name__)


@log.route('/')
@log.route('/<int:log_type>')
def index(log_type=LogType.IP):
    log_type = LogType(log_type)
    log_lines = get_log(log_type)

    return render_template('log.html', log_lines=log_lines)

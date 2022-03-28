from flask import Flask
from view.ctrl import ctrl
from view.log import log
from view.black import black

from lib.mqtt import run_mqtt

app = Flask(__name__)

app.register_blueprint(ctrl, url_prefix='/ctrl')
app.register_blueprint(log, url_prefix='/ctrl/log')
app.register_blueprint(black, url_prefix='/ctrl/black')

run_mqtt()

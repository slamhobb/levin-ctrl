from flask import Flask
from view.ctrl import ctrl
from view.log import log

app = Flask(__name__)

app.register_blueprint(ctrl, url_prefix='/ctrl')
app.register_blueprint(log, url_prefix='/ctrl/log')

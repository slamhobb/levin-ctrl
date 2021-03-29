from flask import Flask
from ctrl import ctrl

app = Flask(__name__)

app.register_blueprint(ctrl, url_prefix="/ctrl")

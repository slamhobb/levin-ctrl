from flask import render_template, Blueprint
from lib.router import get_black_list

black = Blueprint('black', __name__)


@black.route('/')
def index():
    black_list = get_black_list()

    return render_template('black.html', black_list=black_list)

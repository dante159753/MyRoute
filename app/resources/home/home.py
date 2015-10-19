from flask.ext.login import login_required, current_user
from flask import render_template
from . import home_blueprint


@home_blueprint.route('/home/')
def home():
    return render_template('index.html')


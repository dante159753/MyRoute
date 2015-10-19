from flask.ext.login import login_required, current_user
from flask import render_template
from . import home_blueprint
from app.helpers.route import RouteHelper


@home_blueprint.route('/home/')
def home():
    routes = RouteHelper.get_all()
    return render_template('index.html', routes=routes)


from flask.ext.login import login_required, current_user
from flask import render_template
from . import home_blueprint
from app.helpers.category import CategoryHelper
from app.helpers.route import RouteHelper


@home_blueprint.route('/home/')
def home():
    rec_categorys = CategoryHelper.get_hot_categorys()
    rec_row1 = rec_categorys[:3]
    rec_row2 = rec_categorys[3:6]
    stat = {}
    stat['unfinished'] = RouteHelper.get_stat(False)
    stat['finished'] = RouteHelper.get_stat(True)
    return render_template('index-after-login.html', rec_row1=rec_row1, rec_row2=rec_row2, stat=stat)

@home_blueprint.route('/')
def intro():
    return render_template('index.html')


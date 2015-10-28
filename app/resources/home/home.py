from flask.ext.login import login_required, current_user
from flask import render_template, request
from . import home_blueprint
from app.helpers.category import CategoryHelper
from app.helpers.user import UserHelper


@home_blueprint.route('/home/')
@login_required
def home():
    rec_categorys = CategoryHelper.get_hot_categorys()
    rec_row1 = rec_categorys[:3]
    rec_row2 = rec_categorys[3:6]
    stat = dict()
    stat['unfinished'] = UserHelper.get_stat(False)
    stat['finished'] = UserHelper.get_stat(True)
    avatar = current_user.avatar.read()
    return render_template('index-after-login.html', rec_row1=rec_row1, rec_row2=rec_row2, stat=stat, avatar=avatar)


@home_blueprint.route('/')
def intro():
    regis_error = 1 if 'regis_error' in request.args else None
    login_error = 1 if 'login_error' in request.args else None
    return render_template('index.html', login_error=login_error, regis_error=regis_error)


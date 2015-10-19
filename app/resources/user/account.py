from flask.ext.login import login_required, login_user, logout_user
from flask import render_template, redirect, flash, url_for, request
from app.helpers.user import UserHelper
from . import user_blueprint


@user_blueprint.route('/login/', methods=['POST'])
def login():
    try:
        assert 'email' in request.form
        assert 'password' in request.form
    except AssertionError:
        flash('please input email and password')
        return redirect(url_for('home.home'))
    user_to_login = UserHelper.get_by_email(request.form['email'])
    if user_to_login == None or not UserHelper.verify_password(user_to_login, request.form['password']):
        flash('invalid email or password')
        return redirect(url_for('home.home'))
    
    # email and password is correct
    login_user(user_to_login)
    return redirect(url_for('home.home'))


@user_blueprint.route('/logout/', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('home.home'))


@user_blueprint.route('/register/', methods=['POST'])
def register():
    try:
        assert 'email' in request.form
        assert 'password' in request.form
        assert 'password_conf' in request.form
        assert request.form['password'] == request.form['password_conf']
        assert 'gender' in request.form
    except AssertionError:
        flash('please input all necessary info')
        return redirect(url_for('home.home'))

    if UserHelper.get_by_email(request.form['email']) != None:
        flash('the email has been registered!')
        return redirect(url_for('home.home'))

    gender = 0 if request.form['gender'] == 'male' else 1

    new_user = UserHelper.create_user(request.form['email'], request.form['password'], gender)
    login_user(new_user)
    return redirect(url_for('home.home'))



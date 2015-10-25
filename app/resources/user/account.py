#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask.ext.login import login_required, login_user, logout_user
from flask import render_template, redirect, flash, url_for, request
from app.helpers.user import UserHelper
from . import user_blueprint
from app.app import login_manager
from app.helpers.parameter import check_form_para


@user_blueprint.route('/login/', methods=['POST'])
def login():
    try:
        check_form_para(['email', 'password'])
    except AssertionError:
        flash(u'请输入邮箱和密码')
        return redirect(url_for('home.home'))

    user_to_login = UserHelper.get_by_email(request.form['email'])
    if user_to_login == None or not UserHelper.verify_password(user_to_login, request.form['password']):
        flash(u'无效的邮箱或密码')
        return redirect(url_for('home.home'))
    
    is_remember = False if 'remember_me' not in request.form else True

    login_user(user_to_login, remember=is_remember)
    return redirect(url_for('home.home'))


@user_blueprint.route('/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))


@user_blueprint.route('/register/', methods=['POST'])
def register():
    try:
        check_form_para(['nickname', 'email', 'password', 'password_conf', 'gender'])
        assert request.form['password'] == request.form['password_conf'], u'两次密码输入不一致，请重新输入'
    except AssertionError, e:
        if e.message:
            flash(e.message)
        else :
            flash(u'请输入所有信息')
        return redirect(url_for('home.home'))

    if UserHelper.get_by_email(request.form['email']) != None:
        flash(u'此邮箱已经被注册，请尝试登录')
        return redirect(url_for('home.home'))

    if len(request.form['nickname']) < 5:
        flash(u'昵称过短，至少需要 5 个字符')
        return redirect(url_for('home.home'))

    gender = 0 if request.form['gender'] == 'male' else 1

    new_user = UserHelper.create_user(request.form['nickname'], request.form['email'], request.form['password'], gender)

    login_user(new_user)

    return redirect(url_for('home.home'))



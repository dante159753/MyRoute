from flask.ext.restful import Resource, reqparse
from flask.ext.login import login_required, login_user
from flask import render_template, redirect, flash, url_for
from app.helpers.header import add_response_headers
from app.helpers.user import UserHelper

__all__ = ['LoginRes', 'LogoutRes', 'RegisterRes']


class LoginRes(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('email', type=unicode, required=True)
    post_parser.add_argument('password', type=unicode, required=True)
    post_parser.add_argument('remember_me', type=lambda x:True if x == 'remember' else False, required=True)

    def post(self):
        args = self.post_parser.parse_args()

        user_to_login = UserHelper.get_by_email(args['email'])
        if user_to_login == None or not UserHelper.verify_password(user_to_login, args['password']):
            flash('invalid email or password')
            return redirect(url_for('home.homeres'))
        
        # email and password is correct
        login_user(user_to_login)
        return redirect(url_for('home.homeres'))


class LogoutRes(Resource):
    def post(self):
        logout_user()
        return redirect(url_for('home.homeers'))


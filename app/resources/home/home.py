from flask.ext.restful import Resource, reqparse
from flask.ext.login import login_required
from flask import render_template
from app.helpers.header import add_response_headers

__all__ = ['HomeRes']


class HomeRes(Resource):
    #@login_required
    @add_response_headers({'Content-Type': 'text/html'})
    def get(self):
        return render_template('index.html')

